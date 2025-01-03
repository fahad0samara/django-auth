from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=[
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
    ])
    notes = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.name} - {self.type} - {self.date}"

class Task(models.Model):
    title = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='pending')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CustomerSegment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    criteria = models.JSONField(help_text="JSON criteria for segment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_customers(self):
        from django.db.models import Q
        import operator
        
        criteria = self.criteria
        query = Q()
        
        if 'company' in criteria:
            query &= Q(company__icontains=criteria['company'])
        if 'created_after' in criteria:
            query &= Q(created_at__gte=criteria['created_after'])
        if 'created_before' in criteria:
            query &= Q(created_at__lte=criteria['created_before'])
        if 'min_tasks' in criteria:
            query &= Q(tasks__count__gte=criteria['min_tasks'])
        if 'min_contacts' in criteria:
            query &= Q(contacts__count__gte=criteria['min_contacts'])
            
        return Customer.objects.filter(query).distinct()

class Report(models.Model):
    REPORT_TYPES = [
        ('customer_activity', 'Customer Activity'),
        ('task_summary', 'Task Summary'),
        ('contact_analysis', 'Contact Analysis'),
        ('segment_analysis', 'Segment Analysis'),
    ]
    
    GROUP_BY_CHOICES = [
        ('day', 'Daily'),
        ('week', 'Weekly'),
        ('month', 'Monthly'),
        ('quarter', 'Quarterly'),
        ('year', 'Yearly'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_run = models.DateTimeField(null=True, blank=True)
    
    # Report Parameters
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    group_by = models.CharField(max_length=20, choices=GROUP_BY_CHOICES, default='month')
    include_inactive = models.BooleanField(default=False)
    min_interactions = models.IntegerField(default=0)
    max_items = models.IntegerField(default=100)
    
    # Additional Filters
    status_filter = models.CharField(max_length=100, blank=True)
    assignee_filter = models.CharField(max_length=100, blank=True)
    category_filter = models.CharField(max_length=100, blank=True)
    
    # Schedule
    schedule = models.CharField(max_length=50, blank=True, help_text="Cron expression for scheduling")
    
    def __str__(self):
        return f"{self.name} ({self.report_type})"
    
    def get_parameters(self):
        """Convert individual fields to parameters dict for report generation"""
        params = {
            "start_date": self.start_date.strftime("%Y-%m-%d") if self.start_date else None,
            "end_date": self.end_date.strftime("%Y-%m-%d") if self.end_date else None,
            "group_by": self.group_by,
            "include_inactive": self.include_inactive,
            "min_interactions": self.min_interactions,
            "max_items": self.max_items,
        }
        
        if self.status_filter:
            params["status"] = self.status_filter
        if self.assignee_filter:
            params["assignee"] = self.assignee_filter
        if self.category_filter:
            params["category"] = self.category_filter
            
        return params

class CustomerNote(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notes')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Note for {self.customer.name} - {self.created_at}"

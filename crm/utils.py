import csv
from io import StringIO
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Avg, Sum, Q
from django.db.models.functions import TruncMonth, TruncWeek
import json
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

def export_customers_csv(modeladmin, request, queryset):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Email', 'Phone', 'Company', 'Created At'])
    
    for customer in queryset:
        writer.writerow([
            customer.name,
            customer.email,
            customer.phone,
            customer.company,
            customer.created_at.strftime('%Y-%m-%d')
        ])
    
    output.seek(0)
    response = HttpResponse(output, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=customers.csv'
    return response

def generate_report(report):
    """Generate report based on type and parameters"""
    from .models import Customer, Contact, Task, CustomerSegment
    
    if report.report_type == 'customer_activity':
        return generate_customer_activity_report(report.parameters)
    elif report.report_type == 'task_summary':
        return generate_task_summary_report(report.parameters)
    elif report.report_type == 'contact_analysis':
        return generate_contact_analysis_report(report.parameters)
    elif report.report_type == 'segment_analysis':
        return generate_segment_analysis_report(report.parameters)
    
def generate_customer_activity_report(parameters):
    from .models import Customer, Contact, Task
    
    start_date = datetime.strptime(parameters.get('start_date', '2000-01-01'), '%Y-%m-%d')
    end_date = datetime.strptime(parameters.get('end_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
    
    customers = Customer.objects.filter(created_at__range=[start_date, end_date])
    
    # Activity metrics
    activity_data = customers.annotate(
        task_count=Count('tasks'),
        contact_count=Count('contacts'),
        avg_task_completion=Avg('tasks__status')
    )
    
    # Create visualizations
    plt.figure(figsize=(15, 10))
    
    # Task distribution
    plt.subplot(2, 2, 1)
    task_data = [d.task_count for d in activity_data]
    plt.hist(task_data, bins=20)
    plt.title('Task Distribution')
    
    # Contact distribution
    plt.subplot(2, 2, 2)
    contact_data = [d.contact_count for d in activity_data]
    plt.hist(contact_data, bins=20)
    plt.title('Contact Distribution')
    
    # Save plot to buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Encode the image
    graphic = base64.b64encode(image_png).decode('utf-8')
    
    return {
        'summary': {
            'total_customers': customers.count(),
            'avg_tasks': sum(task_data) / len(task_data) if task_data else 0,
            'avg_contacts': sum(contact_data) / len(contact_data) if contact_data else 0,
        },
        'visualization': graphic
    }

def generate_task_summary_report(parameters):
    from .models import Task
    
    tasks = Task.objects.all()
    
    # Task status distribution
    status_dist = tasks.values('status').annotate(count=Count('id'))
    
    # Task completion over time
    tasks_by_date = tasks.annotate(
        week=TruncWeek('created_at')
    ).values('week').annotate(count=Count('id')).order_by('week')
    
    # Create visualization
    plt.figure(figsize=(15, 5))
    
    # Status distribution pie chart
    plt.subplot(1, 2, 1)
    status_labels = [s['status'] for s in status_dist]
    status_counts = [s['count'] for s in status_dist]
    plt.pie(status_counts, labels=status_labels, autopct='%1.1f%%')
    plt.title('Task Status Distribution')
    
    # Tasks over time
    plt.subplot(1, 2, 2)
    dates = [d['week'] for d in tasks_by_date]
    counts = [d['count'] for d in tasks_by_date]
    plt.plot(dates, counts)
    plt.title('Tasks Over Time')
    plt.xticks(rotation=45)
    
    # Save plot
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png).decode('utf-8')
    
    return {
        'summary': {
            'total_tasks': tasks.count(),
            'status_distribution': list(status_dist),
        },
        'visualization': graphic
    }

def send_task_notification(task):
    subject = f'New Task Assigned: {task.title}'
    message = f"""
    Hello {task.assigned_to.get_full_name()},

    A new task has been assigned to you:

    Title: {task.title}
    Customer: {task.customer.name}
    Due Date: {task.due_date}
    Description: {task.description}

    Please log in to the CRM to view more details.
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [task.assigned_to.email],
        fail_silently=False,
    )

def get_dashboard_data():
    from .models import Customer, Task, Contact
    
    # Get date ranges
    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)
    
    # Customer statistics
    total_customers = Customer.objects.count()
    new_customers = Customer.objects.filter(created_at__gte=thirty_days_ago).count()
    
    # Task statistics
    tasks_by_status = list(Task.objects.values('status').annotate(count=Count('id')))
    
    # Contact statistics
    contacts_by_type = list(Contact.objects.filter(
        date__gte=thirty_days_ago
    ).values('type').annotate(count=Count('id')))
    
    # Customer growth (last 6 months)
    six_months_ago = today - timedelta(days=180)
    customer_growth = list(
        Customer.objects.filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    return {
        'total_customers': total_customers,
        'new_customers': new_customers,
        'tasks_by_status': tasks_by_status,
        'contacts_by_type': contacts_by_type,
        'customer_growth': customer_growth
    }

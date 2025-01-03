from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
import json
from django.utils import timezone
from django.http import HttpResponse

from .models import Customer, Contact, Task, Report, CustomerSegment, CustomerNote
from .forms import (
    CustomerForm, ContactForm, TaskForm, CustomerSearchForm,
    ReportForm, SegmentForm, CustomerNoteForm, UserRegistrationForm
)
from .utils import send_task_notification, get_dashboard_data, generate_report

# Home view
def home(request):
    if request.user.is_authenticated:
        return redirect('crm:dashboard')
    return render(request, 'home.html')

# Dashboard views
@login_required
def dashboard(request):
    # Get dashboard data
    data = get_dashboard_data()
    
    # Convert data for charts
    chart_data = {
        'tasks': json.dumps(data['tasks_by_status']),
        'contacts': json.dumps(data['contacts_by_type']),
        'growth': json.dumps([{
            'month': item['month'].strftime('%Y-%m'),
            'count': item['count']
        } for item in data['customer_growth']])
    }
    
    context = {
        'customer_count': data.get('total_customers', 0),
        'new_customers': data.get('new_customers', 0),
        'recent_contacts': Contact.objects.select_related('customer').order_by('-date')[:5],
        'pending_tasks': Task.objects.filter(status='pending').select_related('customer')[:5],
        'chart_data': chart_data,
    }
    return render(request, 'crm/dashboard.html', context)

# Customer views
@login_required
def customers(request):
    customers = Customer.objects.all()
    return render(request, 'crm/customers.html', {'customers': customers})

@login_required
def customer_list(request):
    search_form = CustomerSearchForm(request.GET)
    customers = Customer.objects.annotate(
        task_count=Count('tasks'),
        contact_count=Count('contacts')
    )
    
    if search_form.is_valid() and search_form.cleaned_data['query']:
        query = search_form.cleaned_data['query']
        customers = customers.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query)
        )
    
    customers = customers.order_by('-created_at')
    return render(request, 'crm/customer_list.html', {
        'customers': customers,
        'search_form': search_form
    })

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully!')
            return redirect('crm:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'crm/customer_form.html', {'form': form, 'title': 'Add Customer'})

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('crm:customer_detail', pk=pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'crm/customer_form.html', {'form': form, 'title': 'Edit Customer'})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    contacts = customer.contacts.order_by('-date')
    tasks = customer.tasks.order_by('-due_date')
    
    if request.method == 'POST':
        if 'add_contact' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact = contact_form.save(commit=False)
                contact.created_by = request.user
                contact.save()
                messages.success(request, 'Contact added successfully!')
                return redirect('crm:customer_detail', pk=pk)
        elif 'add_task' in request.POST:
            task_form = TaskForm(request.POST)
            if task_form.is_valid():
                task = task_form.save()
                messages.success(request, 'Task added successfully!')
                return redirect('crm:customer_detail', pk=pk)
    
    contact_form = ContactForm(initial={'customer': customer})
    task_form = TaskForm(initial={'customer': customer, 'assigned_to': request.user})
    
    return render(request, 'crm/customer_detail.html', {
        'customer': customer,
        'contacts': contacts,
        'tasks': tasks,
        'contact_form': contact_form,
        'task_form': task_form,
    })

# Task views
@login_required
def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'crm/tasks.html', {'tasks': tasks})

@login_required
def task_list(request):
    tasks = Task.objects.select_related('customer', 'assigned_to').order_by('due_date')
    return render(request, 'crm/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user
            task.save()
            
            # Send email notification
            send_task_notification(task)
            
            messages.success(request, 'Task created successfully!')
            return redirect('crm:task_list')
    else:
        form = TaskForm()
    return render(request, 'crm/task_form.html', {'form': form, 'title': 'Add Task'})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('crm:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'crm/task_form.html', {'form': form, 'title': 'Edit Task'})

# Report views
@login_required
def report_list(request):
    reports = Report.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'crm/report_list.html', {'reports': reports})

@login_required
def report_create(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user
            report.save()
            messages.success(request, f'Report "{report.name}" has been created successfully!')
            if request.headers.get('HX-Request'):
                return HttpResponse(status=204, headers={'HX-Trigger': 'reportCreated'})
            return redirect('crm:report_list')
    else:
        form = ReportForm()
    
    context = {
        'form': form,
        'title': 'Create New Report',
    }
    return render(request, 'crm/report_form.html', context)

@login_required
def report_edit(request, pk):
    report = get_object_or_404(Report, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated successfully!')
            return redirect('crm:report_view', pk=pk)
    else:
        form = ReportForm(instance=report)
    return render(request, 'crm/report_form.html', {'form': form, 'title': 'Edit Report'})

@login_required
def report_view(request, pk):
    report = get_object_or_404(Report, pk=pk, created_by=request.user)
    report_data = None
    if report.last_run:
        report_data = generate_report(report)
    return render(request, 'crm/report_view.html', {
        'report': report,
        'report_data': report_data
    })

@login_required
def report_run(request, pk):
    report = get_object_or_404(Report, pk=pk, created_by=request.user)
    report.last_run = timezone.now()
    report.save()
    messages.success(request, 'Report generated successfully!')
    return redirect('crm:report_view', pk=pk)

# Segment views
@login_required
def segment_list(request):
    segments = CustomerSegment.objects.all().annotate(
        customer_count=Count('get_customers')
    )
    return render(request, 'crm/segment_list.html', {'segments': segments})

@login_required
def segment_create(request):
    if request.method == 'POST':
        form = SegmentForm(request.POST)
        if form.is_valid():
            segment = form.save()
            messages.success(request, 'Segment created successfully!')
            return redirect('crm:segment_view', pk=segment.pk)
    else:
        form = SegmentForm()
    return render(request, 'crm/segment_form.html', {'form': form, 'title': 'Create Segment'})

@login_required
def segment_view(request, pk):
    segment = get_object_or_404(CustomerSegment, pk=pk)
    customers = segment.get_customers()
    return render(request, 'crm/segment_view.html', {
        'segment': segment,
        'customers': customers
    })

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login to continue.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# Static views
def privacy_policy(request):
    """View for the privacy policy page."""
    return render(request, 'pages/privacy.html')

def terms_of_service(request):
    """View for the terms of service page."""
    return render(request, 'pages/terms.html')

def contact_us(request):
    """View for the contact us page."""
    return render(request, 'pages/contact.html')

from django import forms
from django.contrib.auth.models import User
from .models import Customer, Contact, Task, Report, CustomerSegment, CustomerNote
import json
from datetime import datetime, timedelta

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'company']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['customer', 'type', 'notes']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'customer', 'description', 'due_date', 'status', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

class CustomerSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search customers...'})
    )

class ReportForm(forms.ModelForm):
    SCHEDULE_CHOICES = [
        ('', 'No schedule (run manually)'),
        ('0 0 * * *', 'Daily at midnight'),
        ('0 0 * * 0', 'Weekly on Sunday'),
        ('0 0 1 * *', 'Monthly on 1st'),
        ('0 9 * * 1-5', 'Weekdays at 9 AM'),
        ('custom', 'Custom Schedule')
    ]

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a descriptive name for your report'
        }),
        help_text='Choose a clear name that describes the purpose of this report'
    )

    report_type = forms.ChoiceField(
        choices=Report.REPORT_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text='Select the type of report you want to generate'
    )

    schedule = forms.ChoiceField(
        choices=SCHEDULE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'schedule_select'
        }),
        help_text='Choose when to run this report automatically'
    )

    custom_schedule = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'custom_schedule',
            'placeholder': 'Enter custom cron expression (e.g., 0 0 * * *)'
        }),
        help_text='Format: minute hour day month weekday'
    )

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=True,
        help_text='When should the report start collecting data?'
    )
    
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=True,
        help_text='When should the report stop collecting data?'
    )
    
    min_interactions = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '1000',
            'step': '1'
        }),
        initial=0,
        required=False,
        help_text='Minimum number of interactions to include (0-1000)'
    )
    
    max_items = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '1000',
            'step': '1'
        }),
        initial=100,
        required=False,
        help_text='Maximum number of items to include (1-1000)'
    )

    status_filter = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., pending,in_progress'
        }),
        help_text='Enter status values separated by commas'
    )

    assignee_filter = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or "current_user"'
        }),
        help_text='Filter by assignee username'
    )

    category_filter = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., high_priority,urgent'
        }),
        help_text='Enter categories separated by commas'
    )
    
    class Meta:
        model = Report
        fields = [
            'name', 'report_type', 'start_date', 'end_date', 
            'group_by', 'include_inactive', 'min_interactions', 
            'max_items', 'status_filter', 'assignee_filter', 
            'category_filter'
        ]
        widgets = {
            'group_by': forms.Select(attrs={
                'class': 'form-control'
            }),
            'include_inactive': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        help_texts = {
            'group_by': 'How should the data be grouped?',
            'include_inactive': 'Include inactive items in the report?'
        }
        error_messages = {
            'name': {
                'required': 'Please enter a name for your report',
                'max_length': 'Report name cannot exceed 100 characters'
            },
            'report_type': {
                'required': 'Please select a report type'
            },
            'start_date': {
                'required': 'Please select a start date'
            },
            'end_date': {
                'required': 'Please select an end date'
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Validate dates
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date must be after start date")
            if (end_date - start_date).days > 365:
                raise forms.ValidationError("Date range cannot exceed 1 year")

        # Validate numeric fields
        min_interactions = cleaned_data.get('min_interactions')
        max_items = cleaned_data.get('max_items')
        if min_interactions is not None and min_interactions < 0:
            raise forms.ValidationError("Minimum interactions cannot be negative")
        if max_items is not None and max_items < 1:
            raise forms.ValidationError("Maximum items must be at least 1")
        if max_items is not None and max_items > 1000:
            raise forms.ValidationError("Maximum items cannot exceed 1000")

        # Handle schedule validation
        schedule_choice = cleaned_data.get('schedule')
        custom_schedule = cleaned_data.get('custom_schedule')

        if schedule_choice == 'custom':
            if not custom_schedule:
                raise forms.ValidationError({
                    'custom_schedule': "Please enter a custom cron expression"
                })
            schedule = custom_schedule
        else:
            schedule = schedule_choice

        if schedule:
            parts = schedule.split()
            if len(parts) != 5:
                raise forms.ValidationError({
                    'custom_schedule' if schedule_choice == 'custom' else 'schedule': 
                    "Invalid cron expression. Must have 5 parts: minute hour day month weekday"
                })
            
            try:
                minute, hour, day, month, weekday = parts
                
                # Validate minute (0-59)
                if not (minute == '*' or (minute.isdigit() and 0 <= int(minute) <= 59)):
                    raise forms.ValidationError({
                        'custom_schedule' if schedule_choice == 'custom' else 'schedule':
                        "Minute must be between 0 and 59 or *"
                    })
                
                # Validate hour (0-23)
                if not (hour == '*' or (hour.isdigit() and 0 <= int(hour) <= 23)):
                    raise forms.ValidationError({
                        'custom_schedule' if schedule_choice == 'custom' else 'schedule':
                        "Hour must be between 0 and 23 or *"
                    })
                
                # Validate day (1-31)
                if not (day == '*' or (day.isdigit() and 1 <= int(day) <= 31)):
                    raise forms.ValidationError({
                        'custom_schedule' if schedule_choice == 'custom' else 'schedule':
                        "Day must be between 1 and 31 or *"
                    })
                
                # Validate month (1-12)
                if not (month == '*' or (month.isdigit() and 1 <= int(month) <= 12)):
                    raise forms.ValidationError({
                        'custom_schedule' if schedule_choice == 'custom' else 'schedule':
                        "Month must be between 1 and 12 or *"
                    })
                
                # Validate weekday (0-6)
                if not (weekday == '*' or (weekday.isdigit() and 0 <= int(weekday) <= 6)):
                    raise forms.ValidationError({
                        'custom_schedule' if schedule_choice == 'custom' else 'schedule':
                        "Weekday must be between 0 and 6 or *"
                    })
                
            except ValueError:
                raise forms.ValidationError({
                    'custom_schedule' if schedule_choice == 'custom' else 'schedule':
                    "Invalid cron expression format"
                })

        cleaned_data['schedule'] = schedule
        return cleaned_data

class SegmentForm(forms.ModelForm):
    criteria = forms.JSONField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    class Meta:
        model = CustomerSegment
        fields = ['name', 'description', 'criteria']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CustomerNoteForm(forms.ModelForm):
    class Meta:
        model = CustomerNote
        fields = ['content', 'is_private']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'required': 'True'}
    ))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'required': 'True'}
    ))
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'required': 'True'}
    ))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

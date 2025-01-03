from django.contrib import admin
from .models import Customer, Contact, Task
from .utils import export_customers_csv

# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'company', 'created_at')
    search_fields = ('name', 'email', 'company')
    list_filter = ('created_at',)
    actions = [export_customers_csv]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('customer', 'type', 'date', 'created_by')
    list_filter = ('type', 'date')
    search_fields = ('customer__name', 'notes')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'due_date', 'status', 'assigned_to')
    list_filter = ('status', 'due_date', 'assigned_to')
    search_fields = ('title', 'description', 'customer__name')

from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Customer URLs
    path('customers/', views.customers, name='customers'),
    path('customers/list/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    
    # Task URLs
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/list/', views.task_list, name='task_list'),
    path('tasks/add/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    
    # Report URLs
    path('reports/', views.report_list, name='report_list'),
    path('reports/add/', views.report_create, name='report_create'),
    path('reports/<int:pk>/', views.report_view, name='report_view'),
    path('reports/<int:pk>/edit/', views.report_edit, name='report_edit'),
    path('reports/<int:pk>/run/', views.report_run, name='report_run'),
    
    # Segment URLs
    path('segments/', views.segment_list, name='segment_list'),
    path('segments/add/', views.segment_create, name='segment_create'),
    path('segments/<int:pk>/', views.segment_view, name='segment_view'),
    
    # Static pages
    path('privacy/', views.privacy_policy, name='privacy'),
    path('terms/', views.terms_of_service, name='terms'),
    path('contact/', views.contact_us, name='contact'),
]

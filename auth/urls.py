from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from two_factor.urls import urlpatterns as tf_urls
from django.conf import settings
from django.conf.urls.static import static

# Main URL patterns
urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),
    
    # Homepage
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Authentication URLs
    path('', include(tf_urls)),  # Two-factor auth URLs
    path('accounts/', include('allauth.urls')),  # Django Allauth URLs
    
    # CRM URLs
    path('crm/', include('crm.urls')),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

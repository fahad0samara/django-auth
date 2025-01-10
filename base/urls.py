
from . import views
from django.urls import path,include


urlpatterns = [
    path("", views.home ,name="home"),
    path('login_user/', views.login, name='login'),



]
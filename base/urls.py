
from django.urls import path,include
from .views import auth, home

urlpatterns = [
    path("", home ,name="home"),
path("signup/", auth,name="auth"),
 path("accounts/",include("django.contrib.auth.urls"))

]
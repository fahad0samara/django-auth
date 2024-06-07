from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
 return render(request, "home.html",{})


# Create your views here.
def auth(request):
    if request.method == "post":
     form = UserCreationForm(request.POST or None)
     if form.is_valid():
      form.save()
    else:
     form = UserCreationForm()
    return render(request, "registration/login.html", {"form": form}) 

   




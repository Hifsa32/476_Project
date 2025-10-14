from django.shortcuts import render, redirect
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import  login_required

# Create your views here.


# @login_required
def home (request): 
    return render (request, "home.html", {})

def authView (request):
    if request.method == "POST": 
     form = UserCreationForm(request.POST or None)
     if form.is_valid():
        form.save()
        return redirect('accounts:login') 
    else:
        form = UserCreationForm()
    return render (request, "accounts/signup.html", {"form" : form})

def login(request):
    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context) 


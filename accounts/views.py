from django.shortcuts import render, redirect
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import  login_required
from django.contrib import auth 
from django.contrib.auth.models import User 
from posts.models import Post


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
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
      
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('posts:home') 
        
    else:

        form = AuthenticationForm()
        
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout (request): 
    auth.logout(request)
    return redirect('posts:home') 


@login_required 
def profile (request): 
<<<<<<< HEAD
    user = request.user
    user_posts = Post.objects.filter(author=user).order_by('-date_time')

    
    context = {
        'profile_user': user,
        'user_posts': user_posts,
    }
    
    
    return render(request, 'accounts/profile.html', context)
=======
      return render (request, "accounts/profile.html", {})

def settings(request):
    return render(request, "accounts/settings.html")
>>>>>>> origin/main

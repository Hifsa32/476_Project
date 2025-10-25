from django.shortcuts import render, redirect
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import  login_required
from django.contrib import auth 
from django.contrib.auth.models import User 
from posts.models import Post
from .forms import UserUpdateForm, ProfileForm,  SecurityForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash


from accounts.models import Profile 

def authView (request):
    if request.method == "POST": 
     form = UserCreationForm(request.POST or None)
     if form.is_valid():
        form.save()
        return redirect('accounts:login') 
    else:
        form = UserCreationForm()
    return render (request, "accounts/signup.html", {"form" : form})

def login_view(request):
    user = request.user
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


def logout_view (request): 
    auth.logout(request)
    return redirect('posts:home') 

@login_required 
def profile_view (request): 

    user = request.user
    user_posts = Post.objects.filter(author=user).order_by('-date_time')
    user_notifications = user.notifications.all().order_by('-created_at')

    context = {
        'profile_user': user,
        'user_posts': user_posts,
        'user_notifications': user_notifications,
        'has_new_notifications': user.notifications.filter(is_new=True).exists()
    }

    return render(request, 'accounts/profile.html', context)



@login_required
def settings_view(request):
    user = request.user

    if request.method == "POST":
        which = request.POST.get("which")

        if which == "account":
            uform = UserUpdateForm(request.POST, instance=user)
            pform = ProfileForm(instance=user)
            pwform = SecurityForm(user)

            if uform.is_valid():
                uform.save()
                messages.success(request, "Account info updated successfully.")
                return redirect("accounts:settings")
            else:
                messages.error(request, "Something went wrong. Please check the form fields.")
        
        elif which == "profile":
            pform = ProfileForm(request.POST, request.FILES, instance=user.profile)
            uform = UserUpdateForm(instance=user)
            pwform = SecurityForm(user)
            if pform.is_valid():
                pform.save()
                messages.success(request, "Profile details updated successfully.")
                return redirect("accounts:settings")
            else:
                messages.error(request, "Could not update your profile details.")

        elif which == "password":
            pwform = SecurityForm(user, request.POST)
            pform = ProfileForm(instance=user.profile)
            uform = UserUpdateForm(instance=user)
            if pwform.is_valid():
                pwform.save()
                update_session_auth_hash(request, pwform.user)
                messages.success(request, "Password changed successfully.")
                return redirect("accounts:settings")
            else:
                messages.error(request, "Password change failed. Try again.")
    else:
        pform = ProfileForm(instance=user.profile)
        uform = UserUpdateForm(instance=user)
        pwform = SecurityForm(user)

    return render(request, "accounts/settings.html", {
        "pform": pform,
        "uform": uform,
        "pwform": pwform
    })

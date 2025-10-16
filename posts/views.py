from django.shortcuts import render, redirect
from .models import Post 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .forms import PostForm 


def home(request):
    
    posts_to_display = None

    if request.user.is_authenticated:
        posts_to_display = Post.objects.all().order_by('-date_time')
    else:
        posts_to_display = Post.objects.all().order_by('-date_time')[:6]
        
    context = {
        'posts': posts_to_display,
    }
    
    return render(request, 'posts/home.html', context)
   


@login_required 
def create_post(request):

        
    if request.method == 'POST':

        form = PostForm(request.POST)

        if form.is_valid():
  
            new_post = form.save(commit=False)
            
 
            new_post.author = request.user

            new_post.save()
            
            return redirect('posts:home') 

    else:

        form = PostForm()

    context = {
        'form': form,
        'page_title': 'Create New Post'
    }
    
    return render(request, 'posts/new_post.html', context)
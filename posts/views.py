from django.shortcuts import render, redirect
from .models import Post 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .forms import PostForm 


def home(request):

    all_posts = Post.objects.all().order_by('-date_time') 

    context = {
        'posts': all_posts,
        'page_title': 'Unfiltered - Home'
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
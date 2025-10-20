from django.shortcuts import render, redirect
from .models import Post 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .forms import PostForm 
from django.contrib import messages
from .models import Report


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


# Report Post

ALLOWED_REASONS = {"spam","harassment","misinformation","hate","inappropriate","copyright","other"}

def report_page(request):
    if request.method == "POST":
        reasons = [r.strip() for r in request.POST.getlist("reason")]
        reasons = [r for r in reasons if r in ALLOWED_REASONS]

        other_text = (request.POST.get("otherReason") or "").strip()
        details = (request.POST.get("details") or "").strip()

        errors = []

        # 1) must select at least one reason
        if not reasons:
            errors.append("Please select at least one reason.")

        # 2) if 'other' selected, text is required
        if "other" in reasons and not other_text:
            errors.append("Please explain why you are reporting this post.")

        if errors:
            for e in errors:
                messages.error(request, e)
            ctx = {"selected_reasons": set(reasons), "other_text": other_text, "details": details}
            return render(request, "report.html", ctx)

        # save if valid
        Report.objects.create(
            reasons=reasons,
            other_reason=other_text if "other" in reasons else "",
            details=details,
            reporter=request.user if request.user.is_authenticated else None,
        )
        messages.success(request, "Thanks! Your report was submitted.")
        return redirect("posts:report")

    return render(request, "posts/report.html")

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Report, PostReportSubject
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .forms import PostForm 
from django.contrib import messages
from .observers import PostTakedownObserver, AuthorNotificationObserver


def home(request):

    active_posts_query = Post.objects.filter(is_active=True).order_by('-date_time')
    
    posts_to_display = None

    if request.user.is_authenticated:
        posts_to_display = active_posts_query
    else:
        posts_to_display = active_posts_query[:6]
        
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


# Report Post

ALLOWED_REASONS = {"spam","harassment","misinformation","hate","inappropriate","copyright","other"}

def report_post(request, post_id):

    post = get_object_or_404(Post, pk=post_id)
    reporter = request.user

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
            reporter=reporter,
            post=post,              

        )
        report_subject = PostReportSubject(post=post, reporter=reporter)
        report_subject.register(PostTakedownObserver()) 
        report_subject.register(AuthorNotificationObserver())
        report_subject.notify()
        messages.success(request, "Thanks! Your report was submitted.")
        return redirect("posts:report")

    return render(request, "posts/report.html")

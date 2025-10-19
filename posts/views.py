from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Report

# Create your views here.

def home(request):
    return render(request, "settings.html")

def settings_view(request):
    return render(request, "settings.html")

def maps_page(request):
    return render(request, "maps.html")

def create_post_page(request):
    return render(request, "create-post.html")

def profile_page(request):
    return render(request, "profile.html")


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
        return redirect("report")

    return render(request, "report.html")
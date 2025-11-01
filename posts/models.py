
from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from .observers import Subject
from datetime import date

def validate_past_or_present_datetime(value):
    if value.date() > date.today():
        raise ValidationError(
            'Improper Date Value',
            params={'value': value},
        )
    
class Post(models.Model):
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    date_time = models.DateTimeField(validators=[validate_past_or_present_datetime])
    location = models.CharField(max_length=100)


    TAG_CHOICES = [
        ('NATURAL', 'Natural'),
        ('SOCIAL', 'Social'),
        ('POLITICAL', 'Political'),
    ]
    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default='SOCIAL',
    )
    

    def __str__(self):
        return f"{self.tag} post at {self.location} on {self.date_time.strftime('%Y-%m-%d')}"



# Report Page

class Report(models.Model):
    post = models.ForeignKey(
        'Post', 
        on_delete=models.CASCADE,
        related_name='reports'
    )
    
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    reasons = models.JSONField(default=list) 
    other_reason = models.CharField(max_length=200, blank=True)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        who = self.reporter.username if self.reporter else "anon"
        return f"Report by {who} @ {self.created_at:%Y-%m-%d %H:%M}"
    
#Notification Model 
    
class Notification(models.Model):
 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)

    is_read = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif for {self.user.username}: {self.message}"
    
#Concrete Subject 

class PostReportSubject(Subject):
  
    def __init__(self, post, reporter):
        super().__init__()
        self._post = post
        self._reporter = reporter
        self._report_time = timezone.now() 

    def get_state(self):
        return {
            'post': self._post,
            'reporter': self._reporter,
            'time': self._report_time
        }
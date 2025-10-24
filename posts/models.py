
from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    date_time = models.DateTimeField()
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
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    reasons = models.JSONField(default=list)  # stores checkbox values
    other_reason = models.CharField(max_length=200, blank=True)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        who = self.reporter.username if self.reporter else "anon"
        return f"Report by {who} @ {self.created_at:%Y-%m-%d %H:%M}"
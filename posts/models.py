from django.db import models
from django.conf import settings


# Create your models here.


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
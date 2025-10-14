
from django.db import models
from django.contrib.auth.models import User 

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

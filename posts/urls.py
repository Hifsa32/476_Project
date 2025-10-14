from django.urls import path
from .views import home, create_post

app_name = 'posts'

urlpatterns = [
     path("", home, name="home"), 
     path("new/", create_post, name="create_post"),
   
]
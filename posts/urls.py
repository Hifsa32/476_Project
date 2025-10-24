from django.urls import path
from .views import home, create_post
from . import views

app_name = 'posts'

urlpatterns = [
     path("", home, name="home"), 
     path("new/", create_post, name="create_post"),
     path('report/<int:post_id>/', views.report_post, name='report_post'),
   
]
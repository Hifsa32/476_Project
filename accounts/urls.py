
from django.urls import path, include
from .views import authView, login, logout, profile, settings
from . import views

app_name = 'accounts' 

urlpatterns = [
    path("login/", login, name="login"), 
    path("signup/", authView, name = "authView"), 
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("settings/", settings, name="settings"),
    # path("accounts/", include("django.contrib.auth.urls")), 
   
]
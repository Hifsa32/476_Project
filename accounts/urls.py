
from django.urls import path, include
from . import views

app_name = 'accounts' 

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.authView, name="authView"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("settings/", views.settings_view, name="settings"),
]
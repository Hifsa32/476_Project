
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),               
    path("settings/", views.settings_view, name="settings"),
    path("report/", views.report_page, name="report"),
    path("maps/", views.maps_page, name="maps"),
    path("create/", views.create_post_page, name="create_post"),
    path("profile/", views.profile_page, name="profile"),
]

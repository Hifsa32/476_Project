from django.contrib import admin
from .models import Report

# Register your models here.
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "reporter", "created_at")
    list_filter = ("created_at",)
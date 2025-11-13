from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 
from posts.views import db_health

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('', include('posts.urls')), 
    path('__db__/', db_health),     
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
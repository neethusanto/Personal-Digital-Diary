"""
URL configuration for diary_core project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('diary_web.urls')),
]

"""
Project-level URL routing.

This file just says:
- /admin/  -> Django's built-in admin panel
- anything else -> handled by the chatbot app's urls.py
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')),
]

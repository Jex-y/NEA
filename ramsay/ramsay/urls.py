"""
Definition of urls for ramsay.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
]

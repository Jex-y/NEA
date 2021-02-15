from django.urls import path, include
from rest_framework import routers
from ramsay import settings
from .views import *

urlpatterns = [
        path('', MainView),
        ]
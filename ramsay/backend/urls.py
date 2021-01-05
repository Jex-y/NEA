from django.urls import path, include
from rest_framework import routers
from .views import *

urlpatterns = [
        path('menus/', ItemMenuListView.as_view()),
        path('menus/<str:url_name>', ItemMenuListView.as_view()),
        path('items/search=<str:query>', ItemSearchView.as_view(), name='search'),
    ]
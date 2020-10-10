from django.urls import path, include
from rest_framework import routers
from .views import *

urlpatterns = [
        path('menus/', MenuListView.as_view()),
        path('menus/<str:url_name>', ItemMenuListView.as_view()),
        path('items/<int:pk>/', ItemDetailView.as_view()),
        path('items/search=<str:query>', ItemSearchView.as_view(), name='search'),
    ]
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import routers
from .views import *

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('menus/<str:menu>', ItemMenuList.as_view),
    path('items/<int:pk>/', ItemDetail.as_view),
] + static('media/', document_root=settings.MEDIA_ROOT)
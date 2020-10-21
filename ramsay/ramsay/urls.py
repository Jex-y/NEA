from datetime import datetime
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('backend.urls','backend'), namespace='backend')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

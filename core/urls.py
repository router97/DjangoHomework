from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin', admin.site.urls, name = 'admin'),
    path('', include('apps.main.urls', namespace = 'main')),
    path('', include('apps.blog.urls', namespace='blog')),
    path('', include('apps.members.urls', namespace='members')),
    path('catalog/', include('apps.catalog.urls', namespace='catalog')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name = 'admin'),
    path('', include('apps.main.urls', namespace = 'main'), name = 'apps.main'),
]
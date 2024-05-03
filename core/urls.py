from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


handler404 = 'apps.main.views.custom_404'

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('_nested_admin/', include('nested_admin.urls')),
    
    path('admin/', admin.site.urls, name='admin'), 
    
    path('', include('apps.main.urls', namespace='main')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('', include('apps.members.urls', namespace='members')),
    path('order/', include('apps.order.urls', namespace='order')),
    path('catalog/', include('apps.catalog.urls', namespace='catalog')),
    path('quiz/', include('apps.quiz.urls', namespace='quiz')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('favicon.svg/', views.favicon, name='favicon'),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]
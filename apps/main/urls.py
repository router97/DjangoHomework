from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('lol/', views.lolasdasdasd, name='lol123'),
    path('lol2/', views.index, name='lol1234'),
    path('about', views.about, name='about')
]
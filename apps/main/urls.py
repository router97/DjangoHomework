from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('about/', views.about, name='about'),
]
from django.urls import path

from . import views

app_name = 'members'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
from django.urls import path

from . import views

app_name = 'members'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
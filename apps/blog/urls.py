from django.urls import path
from . import views

urlpatterns = [
    path('article/<int:id>/', views.article, name = 'article'),
    path('add-article', views.add_article, name = 'add-article'),
    path('<int:article_id>/like/', views.like, name='like'),
]
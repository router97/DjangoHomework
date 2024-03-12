from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('article/<int:id>/', views.article, name='article'),
    path('add-article/', views.add_article, name='add-article'),
    path('like/<int:article_id>/', views.like, name='like'),
    path('like-comment/<int:comment_id>/', views.like_comment, name='like-comment'),
    path('dislike/<int:article_id>/', views.dislike, name='dislike'),
    path('add-comment/<int:article_id>/', views.add_comment, name='add-comment'),
]
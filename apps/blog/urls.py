from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('article/<int:id>/', views.article, name='article'),
    path('add-article/', views.AddArticleView.as_view(), name='add-article'),
    path('delete-article/<int:id>/', views.delete_article, name='delete-article'),
    path('edit-article/<int:id>/', views.EditArticleView.as_view(), name='edit-article'),
    path('like/<int:article_id>/', views.like_article, name='like'),
    path('like-comment/<int:comment_id>/', views.like_comment, name='like-comment'),
    path('dislike/<int:article_id>/', views.dislike_article, name='dislike'),
    path('add-comment/<int:article_id>/', views.add_comment, name='add-comment'),
]
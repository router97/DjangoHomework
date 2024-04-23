from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.TopicListView.as_view(), name='index'), 
    path('<slug:slug>/', views.QuizByTopicView.as_view(), name='topic'), 
    path('<slug:topic_slug>/<slug:slug>/', views.QuizView.as_view(), name='quiz'), 
    path('submit_answer/<uuid:id>', views.submit_answer, name='submit_answer'), 
]
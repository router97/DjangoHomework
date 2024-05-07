from django.urls import path

from . import views


app_name = 'apps.quiz'

urlpatterns = [
    path('', views.TopicListView.as_view(), name='index'), 
    path('<slug:slug>/', views.SubTopicListView.as_view(), name='topic'), 
    path('<slug:topic_slug>/quizzes/', views.QuizzesByTopicListView.as_view(), name='quizzes'), 
    path('<slug:topic_slug>/<slug:slug>/', views.QuizView.as_view(), name='quiz'), 
    path('submit_answer/<uuid:id>', views.submit_answer, name='submit_answer'), 
]
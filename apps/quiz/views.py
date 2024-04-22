from django.shortcuts import get_object_or_404, redirect
from django.http import HttpRequest
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, View

from .models import Topic, Quiz, ChoiceAnswer


class TopicListView(ListView):
    model = Topic
    template_name = 'quiz/index.html'
    context_object_name = 'topics' 
    
    def get_queryset(self):
        return Topic.objects.filter(parent=None)

class QuizByTopicView(ListView):
    template_name = 'quiz/quiz_by_topic.html'
    context_object_name = 'quizzes'
    
    def get_queryset(self):
        topic = self.kwargs.get('slug')
        descendants = Topic.objects.filter(slug=topic).get_descendants(include_self=True)
        queryset = Quiz.objects.filter(topic__in=descendants)
        return queryset

    # FIXME: weurjnsfm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_slug = self.kwargs['slug']
        topic = get_object_or_404(Topic, slug=topic_slug)
        context['topic'] = topic
        context['topics'] = Topic.objects.filter(parent=topic)
        return context

class QuizView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz.html'
    context_object_name = 'quiz'

@require_POST
def submit_answer(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)
    
    for question in quiz.questions.all().prefetch_related('answers'):
        answer_ids = request.POST.getlist(f'answer{question.id}')
        print(answer_ids)

        selected_answers = ChoiceAnswer.objects.filter(id__in=answer_ids)
        
        correct_answers = selected_answers.filter(is_correct=True)
        
        print(f'selected:{selected_answers}\ncorrect:{correct_answers}')
        if correct_answers == selected_answers:
            print('CORRECT!!')
            
    return redirect('quiz:index')
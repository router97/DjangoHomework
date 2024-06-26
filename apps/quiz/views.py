from uuid import UUID
from random import sample

from django.shortcuts import get_object_or_404, render, HttpResponse
from django.http import HttpRequest
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

from .models import Topic, Quiz, ChoiceAnswer
from .forms import CompletionForm


class TopicListView(ListView):
    model = Topic
    template_name = 'quiz/index.html'
    context_object_name = 'topics' 
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Topic.objects.filter(parent=None)
        for topic in queryset:
            topic.completion = round(topic.get_topic_completion(self.request.user.id))
            topic.empty = bool(not topic.get_amount_of_quizzes())
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quizzes = Quiz.objects.all()
        for quiz in quizzes:
            quiz.completed, quiz.completion_percent = quiz.is_completed_by(self.request.user.id)
        quizzes_amount = quizzes.count()
        creators_ids = quizzes.values('author').distinct()
        creators = User.objects.filter(id__in=creators_ids)
        
        if list(self.object_list) == list(topic for topic in self.object_list if topic.completion == 100):
            context['completion_topics'] = True
        
        context['quizzes'] = sample(list(quizzes), 4 if 4 < quizzes_amount else quizzes_amount)
        context['quizzes_latest'] = quizzes.order_by('-created_at')[:6]
        context['quizzes_top'] = quizzes.order_by('-completions')[:3]
        
        context['creators'] = creators
        context['stats'] = {
            'quizzes': quizzes_amount,
            'topics': Topic.objects.count(),
            'creators': creators.count(),
        }
        return context

class SubTopicListView(ListView):
    model = Topic
    template_name = 'quiz/quiz_by_topic.html'
    context_object_name = 'topics'
    paginate_by = 6
    
    def get_queryset(self):
        topic_slug = self.kwargs['slug']
        topic = get_object_or_404(Topic, slug=topic_slug)
        queryset = Topic.objects.filter(parent=topic)
        for topic in queryset:
            topic.completion = round(topic.get_topic_completion(self.request.user.id))
            topic.empty = bool(not topic.get_amount_of_quizzes())
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        topic_slug = self.kwargs['slug']
        topic = get_object_or_404(Topic, slug=topic_slug)
        
        descendants = topic.get_descendants(include_self=True)
        quizzes = Quiz.objects.filter(topic__in=descendants)
        for quiz in quizzes:
            quiz.completed, quiz.completion_percent = quiz.is_completed_by(self.request.user.id)
        
        if list(self.object_list) == list(topic for topic in self.object_list if topic.completion == 100):
            context['completion_topics'] = True
        
        quizzes_amount = quizzes.count()
        creators_ids = quizzes.values('author').distinct()
        creators = User.objects.filter(id__in=creators_ids)
        
        context['topic'] = topic
        context['quizzes'] = sample(list(quizzes), 4 if 4 < quizzes_amount else quizzes_amount)
        context['quizzes_latest'] = quizzes.order_by('-created_at')[:6]
        context['quizzes_top'] = quizzes.order_by('-completions')[:3]
        
        context['creators'] = creators
        context['stats'] = {
            'quizzes': quizzes_amount,
            'topics': descendants.count()-1,
            'creators': creators.count(),
        }
        return context

class QuizzesByTopicListView(ListView):
    model = Quiz
    template_name = 'quiz/quizzes.html'
    context_object_name = 'quizzes'
    paginate_by = 20
    
    def get_queryset(self):
        topic_slug = self.kwargs['topic_slug']
        topic = get_object_or_404(Topic, slug=topic_slug)
        
        descendants = topic.get_descendants(include_self=True)
        queryset = Quiz.objects.filter(topic__in=descendants)
        for quiz in queryset:
            quiz.completed, quiz.completion_percent = quiz.is_completed_by(self.request.user.id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        topic_slug = self.kwargs['topic_slug']
        topic = get_object_or_404(Topic, slug=topic_slug)
        
        topics = Topic.objects.all()
        topics_amount = topics.count()
        
        context['topic'] = topic
        topics_random = sample(list(topics), 6 if 6 < topics_amount else topics_amount)
        
        for topic_random in topics_random:
            topic_random.completion = round(topic_random.get_topic_completion(self.request.user.id))
        
        context['topics'] = topics_random
        
        return context
    
class QuizView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz.html'
    context_object_name = 'quiz'

# TODO: Make detailed quiz view with option to start (to QuizView)
class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_detail.html'
    context_object_name = 'quiz'

@require_POST
def submit_answer(request: HttpRequest, id: UUID) -> HttpResponse:
    """Handles quiz answer submission and renders the result page.

    Args:
        request (HttpRequest): HTTP request object with POST data.
        id (UUID): UUID of the quiz being submitted.

    Returns:
        HttpResponse: Renders the quiz result page.
    """
    
    quiz = get_object_or_404(Quiz, id=id)
    questions_answers = {}
    all_ids = []
    
    for question in quiz.questions.all():      
        answer_ids = request.POST.getlist(f'answer{question.id}')
        selected_answers = ChoiceAnswer.objects.filter(id__in=answer_ids)
        questions_answers[question] = selected_answers
        all_ids += list(answer_ids)
    
    completion, questions_result = quiz.get_completion(questions_answers, return_questions=True)
    percentage_for_complexity = quiz.get_percentage_value_for_complexity()
    selected_all = ChoiceAnswer.objects.filter(id__in=all_ids)
    
    context = {
        'quiz': quiz,
        'questions_answers': questions_answers,
        'picked': selected_all,
        'completion': completion,
        'percentage_for_complexity': percentage_for_complexity,
        'questions_result': questions_result,
    }
    
    completion_form = CompletionForm(
        data={
            'user': request.user, 
            'quiz': quiz, 
            'percentage': float(completion), 
            'picked_answers': selected_all, 
        }, 
    )
    if completion_form.is_valid():
        completion_form.save()
    
    return render(request, 'quiz/result.html', context)
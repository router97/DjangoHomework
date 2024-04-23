from uuid import UUID

from django.shortcuts import get_object_or_404, render, HttpResponse
from django.http import HttpRequest
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST

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
    
    return render(request, 'quiz/result.html', context)
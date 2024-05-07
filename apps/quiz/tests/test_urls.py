from uuid import uuid4

from django.test import SimpleTestCase
from django.urls import reverse, resolve

from apps.quiz.views import TopicListView, SubTopicListView, QuizzesByTopicListView, QuizView, submit_answer


class TestUrls(SimpleTestCase):
    
    def test_index_url_resolves(self):
        url = reverse('quiz:index')
        self.assertEqual(resolve(url).func.view_class, TopicListView)
    
    def test_topic_url_resolves(self):
        url = reverse('quiz:topic', args=['some-slug'])
        self.assertEqual(resolve(url).func.view_class, SubTopicListView)
    
    def test_quizzes_url_resolves(self):
        url = reverse('quiz:quizzes', args=['some-slug'])
        self.assertEqual(resolve(url).func.view_class, QuizzesByTopicListView)
    
    def test_quiz_url_resolves(self):
        url = reverse('quiz:quiz', args=['some-slug', 'some-slug'])
        self.assertEqual(resolve(url).func.view_class, QuizView)
    
    def test_submit_answer_url_resolves(self):
        url = reverse('quiz:submit_answer', args=[uuid4()])
        self.assertEqual(resolve(url).func, submit_answer)
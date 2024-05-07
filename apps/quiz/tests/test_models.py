from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.urls import reverse
     
from apps.quiz.models import Topic, Quiz, Question, ChoiceAnswer, Completion

class TopicTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser1')

    def tearDown(self) -> None:
        User.objects.all().delete()
        Topic.objects.all().delete()
        Quiz.objects.all().delete()
        Completion.objects.all().delete()

    def test_get_topic_completion(self) -> None:
        """Test get_topic_completion method."""
        
        # 100.0%
        topic_100 = Topic.objects.create(name='Topic 100')
        quiz_100 = Quiz.objects.create(topic=topic_100, name='Quiz 100', author=self.user)
        completion_100 = Completion.objects.create(user=self.user, quiz=quiz_100, percentage=56.1)
        self.assertEqual(topic_100.get_topic_completion(self.user.id), 100.0, "Topic completion should be 100.0%. One quiz existing, one completed.")

        # 50.0%
        topic_50 = Topic.objects.create(name='Topic 50')
        quiz_50_1 = Quiz.objects.create(topic=topic_50, name='Quiz 50 1', author=self.user)
        quiz_50_2 = Quiz.objects.create(topic=topic_50, name='Quiz 50 2', author=self.user)
        completion_50_1 = Completion.objects.create(user=self.user, quiz=quiz_50_1, percentage=22.8)
        self.assertEqual(topic_50.get_topic_completion(self.user.id), 50.0, "Topic completion should be 50.0%. Two quizzes existing, one completed.")

        # 0.0%
        topic_0 = Topic.objects.create(name='Topic 0')
        quiz_0 = Quiz.objects.create(topic=topic_0, name='Quiz 0', author=self.user)
        self.assertEqual(topic_0.get_topic_completion(self.user.id), 0.0, "Topic completion should be 0.0%. One quiz existing, none completed.")

        # No Quizzes
        topic_none = Topic.objects.create(name='Topic No Quizzes')
        self.assertEqual(topic_none.get_topic_completion(self.user.id), 0.0, "Topic completion should be 0.0%. No quizzes existing, none completed.")
        
        # Invalid User
        topic_invalid_user = Topic.objects.create(name='Test Topic Invalid User')
        quiz_invalid_user = Quiz.objects.create(topic=topic_invalid_user, name='Test Quiz Invalid User', author=self.user)
        self.assertEqual(topic_invalid_user.get_topic_completion(69420228), 0.0, "Topic completion should be 0.0%. User ID provided is invalid.")
        
        # 50% Subtopic
        topic_subtopic = Topic.objects.create(name='Test Topic Subtopic')
        topic_subtopic_subtopic1 = Topic.objects.create(name='Test Topic Subtopic Subtopic 1', parent=topic_subtopic)
        topic_subtopic_subtopic2 = Topic.objects.create(name='Test Topic Subtopic Subtopic 2', parent=topic_subtopic)
        quiz_subtopic1 = Quiz.objects.create(topic=topic_subtopic_subtopic1, name='Test Quiz Subtopic 1', author=self.user)
        quiz_subtopic2 = Quiz.objects.create(topic=topic_subtopic_subtopic2, name='Test Quiz Subtopic 2', author=self.user)
        completion_subtopic1 = Completion.objects.create(user=self.user, quiz=quiz_subtopic1, percentage=31.2)
        self.assertEqual(topic_subtopic.get_topic_completion(self.user.id), 50.0, "Topic completion should be 50.0%. No quizzes in the topic, two quizzes in it's subtopics. One quiz completed.")
        self.assertEqual(topic_subtopic_subtopic1.get_topic_completion(self.user.id), 100.0, "Topic completion should be 100.0%. One quiz existing, one completed.")
        self.assertEqual(topic_subtopic_subtopic2.get_topic_completion(self.user.id), 0.0, "Topic completion should be 0.0%. One quiz existing, none completed.")
    
    def test_get_related_topics(self) -> None:
        """Test get_related_topics method."""
        
        topic_main = Topic.objects.create(name='Test Topic Main')
        topic_sub1 = Topic.objects.create(name='Test Topic Sub 1', parent=topic_main)
        topic_sub2 = Topic.objects.create(name='Test Topic Sub 2', parent=topic_main)
        topic_sub1_sub1 = Topic.objects.create(name='Test Topic Sub 1 Sub 1', parent=topic_sub1)
        topic_sub1_sub2 = Topic.objects.create(name='Test Topic Sub 1 Sub 2', parent=topic_sub1)
        self.assertQuerySetEqual(topic_main.get_related_topics(), [], ordered=False, msg="Topic has subtopics, no parent topic, no sibling topics.")
        self.assertQuerySetEqual(topic_sub1.get_related_topics(), [topic_sub2], ordered=False, msg="Topic has subtopics, a parent topic, a sibling topic.")
        self.assertQuerySetEqual(topic_sub1_sub1.get_related_topics(), [topic_sub1_sub2], ordered=False, msg="Topic doesn't have subtopics, a parent topic with a parent topic, a sibling topic.")
    
    def test_get_amount_of_quizzes(self) -> None:
        """Test get_amount_of_quizzes method."""
        
        topic_main = Topic.objects.create(name='Test Topic Main')
        topic_sub1 = Topic.objects.create(name='Test Topic Sub 1', parent=topic_main)
        topic_sub2 = Topic.objects.create(name='Test Topic Sub 2', parent=topic_main)
        topic_sub1_sub = Topic.objects.create(name='Test Topic Sub 1 Sub', parent=topic_sub1)
        
        topic_main_quiz = Quiz.objects.create(topic=topic_main, name='Test Topic Main Quiz', author=self.user)
        topic_sub1_quiz = Quiz.objects.create(topic=topic_sub1, name='Test Topic Sub 1 Quiz', author=self.user)
        topic_sub1_sub_quiz = Quiz.objects.create(topic=topic_sub1_sub, name='Test Topic Sub 1 Sub Quiz', author=self.user)
        
        self.assertEqual(topic_main.get_amount_of_quizzes(), 3, "Amount of quizzes should be 3. One quiz in the topic itself, one in it's subtopic and one in the subtopic's subtopic.")
        self.assertEqual(topic_sub1.get_amount_of_quizzes(), 2, "Amount of quizzes should be 2. One quiz in the topic itself, one it it's subtopic.")
        self.assertEqual(topic_sub1_sub.get_amount_of_quizzes(), 1, "Amount of quizzes should be 1. One quiz in the topic itself, no subtopics.")
        self.assertEqual(topic_sub2.get_amount_of_quizzes(), 0, "Amount of quizzes should be 0. No quizzes in the topic itself, no subtopics.")
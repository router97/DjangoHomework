import uuid

from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

from mptt.models import MPTTModel, TreeForeignKey

from PIL import Image


class Quiz(models.Model):
    id = models.UUIDField(
        verbose_name='ID', 
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
    )
    topic = models.ForeignKey(
        to='Topic',
        on_delete=models.CASCADE,
        related_name='quizzes', 
        verbose_name='Topic', 
        blank=True, 
        null=True, 
        help_text='Choose the topic of the quiz.', 
    )
    author = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        related_name='quizzes',
        verbose_name='Author', 
        null=True,
        default=None, 
    )
    name = models.CharField(
        verbose_name='Name', 
        max_length=50, 
        editable='True', 
        help_text='Enter the name of the quiz.', 
    )
    slug = models.SlugField(
        verbose_name='URL', 
        max_length=255, 
        unique=True, 
        help_text='A unique slug for the quiz.', 
    )
    short_description = models.TextField(
        verbose_name='Short Description', 
        max_length='100', 
        blank=True, 
        null=True, 
        editable=True, 
        help_text='Enter a short description of the quiz.', 
    )
    description = models.TextField(
        verbose_name='Description', 
        max_length='1000', 
        blank=True, 
        null=True, 
        editable=True, 
        help_text='Enter a description of the quiz.', 
    )
    created_at = models.DateTimeField(
        verbose_name='Created at', 
        auto_now_add=True, 
    )
    edited_at = models.DateTimeField(
        verbose_name='Edited at', 
        auto_now=True, 
    )
    
    def get_absolute_url(self):
        return reverse('quiz:quiz', kwargs={'topic_slug': self.topic.slug, 'slug': self.slug})
    
    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
        ordering = ['name']
    
class Topic(MPTTModel):
    id = models.UUIDField(
        verbose_name='ID', 
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
    )
    parent = TreeForeignKey(
        to='self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children', 
        verbose_name='Parent Topic', 
    )
    name = models.CharField(
        verbose_name='Name', 
        max_length=255, 
        editable=True, 
        help_text='Enter the name of the topic.', 
    )
    image = models.ImageField(
        verbose_name='Image', 
        upload_to='quiz/topic/', 
        blank=True, 
        null=True, 
        help_text='Upload an image for the category.', 
    )
    slug = models.SlugField(
        verbose_name='URL', 
        max_length=255, 
        unique=True, 
        help_text='A unique slug for the topic.', 
    )
    short_description = models.TextField(
        verbose_name='Short Description', 
        max_length='100', 
        blank=True, 
        null=True, 
        editable=True, 
        help_text='Enter a short description of the topic.', 
    )
    description = models.TextField(
        verbose_name='Description', 
        max_length='1000', 
        blank=True, 
        null=True, 
        editable=True, 
        help_text='Enter a description of the topic.', 
    )

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" />')
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    
    def get_absolute_url(self):
        return reverse('quiz:topic', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.image:
            super().save(*args, **kwargs)
            img = Image.open(self.image.path)
            max_size = (450, 300)
            img.thumbnail(max_size)
            img.save(self.image.path)
        super().save(*args, **kwargs)
    
    # TODO: sigm
    def get_complexity(self):
        pass
    
    class MPTTMeta:
        order_insertion_by = ['name']
        
    def __str__(self):
        return self.name

class Question(models.Model):
    COMPLEXITY_CHOICES = (
        ('1', 'Easy'),
        ('2', 'Medium'),
        ('3', 'Hard'),
    )
    TYPE_CHOICES = (
        ('choice', 'Choice'),
    )
    
    text = models.TextField(
        verbose_name='Question Text', 
        max_length=500, 
        editable=True, 
        help_text='Enter the question.'
    )
    quiz = models.ForeignKey(
        to=Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        help_text='Choose a quiz this question belongs to.'
    )
    complexity = models.CharField( 
        max_length = 20, 
        choices = COMPLEXITY_CHOICES, 
        default = '1'
    )
    # type = models.CharField( 
    #     max_length = 20, 
    #     choices = COMPLEXITY_CHOICES, 
    #     default = '1'
    # )
    
    def has_multiple_answers(self) -> bool:
        return self.answers.filter(is_correct=True).count() > 1
    
    def save(self, *args, **kwargs) -> None:
        answers: QuerySet[ChoiceAnswer] = self.answers.all()

        # Check if there are any answers provided at all
        if not answers:
            return
        
        # Check if there is more than 1 answer
        if answers.count() <= 1:
            return
        
        # Check if there is at least a single correct answer
        if not answers.filter(is_correct=True).exists():
            return
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['quiz']

class ChoiceAnswer(models.Model):
    text = models.CharField(
        verbose_name='Answer Text',
        max_length=255,
    )
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    is_correct = models.BooleanField(
        verbose_name='Is Correct?',
        default=False,
    )

    class Meta:
        verbose_name = 'Choice Answer'
        verbose_name_plural = 'Choice Answers'
        ordering = ['question']
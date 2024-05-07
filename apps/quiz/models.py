import uuid
import os

from django.db import models
from django.urls import reverse
from django.db.models import QuerySet
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import SafeText, mark_safe
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from PIL import Image
from mptt.models import MPTTModel, TreeForeignKey


def generate_image_filename(instance: 'Topic', filename: str) -> str:
    """Generate a unique filename for the image."""
    ext = filename.split('.')[-1]
    if instance.slug:
        filename = f'{instance.slug}.{ext}'
    else:
        filename = f'{uuid.uuid4().hex}.{ext}'
    return f'quiz/topic/{filename}'

class CompletionPercentageError(Exception):
    """Raise for errors in calculating completion percentage of a quiz."""

class Quiz(models.Model):
    """
    Represents a quiz.

    Each quiz belongs to a specific topic and belongs to a user.
    """

    id = models.UUIDField(
        verbose_name='ID', 
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        help_text='Unique identifier for the quiz.', 
    )
    topic = models.ForeignKey(
        to='Topic',
        on_delete=models.CASCADE,
        related_name='quizzes', 
        verbose_name='Topic', 
        help_text='Choose the topic of the quiz.', 
    )
    author = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        related_name='quizzes',
        verbose_name='Author', 
        null=True,
        default=None, 
        help_text='The author of the quiz.', 
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
        help_text='The date and time when the quiz was created.', 
    )
    edited_at = models.DateTimeField(
        verbose_name='Edited at', 
        auto_now=True, 
        help_text='The date and time when the quiz was last edited.', 
    )
    
    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
        ordering = ['-edited_at', 'topic']
    
    def get_absolute_url(self) -> str:
        """Returns the URL of the quiz."""
        return reverse('quiz:quiz', kwargs={'topic_slug': self.topic.slug, 'slug': self.slug})
    
    def is_completed_by(self, user_id: int) -> tuple[bool, float]:
        """Check if a user completed the quiz and return completion status and percentage."""
        completion = Completion.objects.filter(quiz=self, user=user_id).first()
        if completion:
            return True, completion.percentage
        return False, 0.0
    
    #TODO: Update algorithm to calculate with complexity weights (value is bigger if the complexity is bigger)
    def get_percentage_value_for_complexity(self) -> dict[str, float]:
        """Returns a dictionary of percentage value of a question of each complexity.

        Returns:
            dict[str, float]: Key is complexity, value is percentage amount for completing a question of such complexity.
        """
        
        total_questions_count: int = self.questions.count()
        percentage_value: float = round(100 / total_questions_count, 1)
        percentage_value_for_complexity: dict[str, float] = {
            '1': percentage_value, 
            '2': percentage_value, 
            '3': percentage_value, 
        }
        return percentage_value_for_complexity

    def get_completion(self, questions_answers: dict, return_questions: bool = False) -> int | tuple[int, dict]:
        """Calculate completion percentage.

        Args:
            questions_answers (dict): Key is Question, value is QuerySet of answers of the user.
            return_questions (bool, optional): Whether to return detailed question completion status. Defaults to False.
        
        Raises:
            CompletionPercentageError: If the completion percent calculated is more than 100%.
        
        Returns:
            int | tuple[int, dict]: Completion percentage or (percentage, question status).
        """
        
        questions_completed = {}
        total_completion = 0
        percentage_value_for_complexity = self.get_percentage_value_for_complexity()
        
        # Calculate total completion and get questions with their results.
        for question, answers in questions_answers.items():
            
            # Get the correct answers for the question
            correct_answers = question.answers.filter(is_correct=True)
            
            # If provided answers were incorrect, mark as incorrect
            if set(correct_answers.values_list('pk', flat=True)) != set(answers.values_list('pk', flat=True)):
                questions_completed[question] = False
                continue
            
            # If correct, increment total completion by question complexity value and mark as completed
            total_completion += percentage_value_for_complexity[question.complexity]
            questions_completed[question] = True
        
        # Round up total completion
        total_completion = round(total_completion)
        if total_completion > 100:
            raise CompletionPercentageError('Total completion is more than 100%')
        return total_completion if not return_questions else (total_completion, questions_completed)
    
    def get_complexity(self) -> int:
        """Returns the average complexity of the questions."""
        
        questions = self.questions.all()
        questions_amount = questions.count()

        # If there are no questions in the quiz return 0
        if questions_amount == 0: 
            return 0

        # Calculate sum of the complexities
        total_complexity = sum(int(complexity) for complexity in questions.values_list('complexity', flat=True))
        return round(total_complexity / questions_amount)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    
class Topic(MPTTModel):
    """
    Represents a topic.

    Topics can be organized using the MPTTModel.
    """
    
    id = models.UUIDField(
        verbose_name='ID', 
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        help_text='Unique identifier for the topic.', 
    )
    parent = TreeForeignKey(
        to='self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children', 
        verbose_name='Parent Topic', 
        help_text='The parent topic if this topic is a sub-topic.', 
    )
    name = models.CharField(
        verbose_name='Name', 
        max_length=255, 
        editable=True, 
        help_text='Enter the name of the topic.', 
    )
    image = models.ImageField(
        verbose_name='Image', 
        upload_to=generate_image_filename, 
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
        max_length=100, 
        blank=True, 
        null=True, 
        editable=True, 
        help_text='Enter a short description of the topic.', 
    )
    description = models.TextField(
        verbose_name='Description', 
        max_length=1000, 
        blank=True, 
        null=True, 
        editable=True, 
        help_text='Enter a description of the topic.', 
    )

    class MPTTMeta:
        order_insertion_by = ['name']
    
    def image_tag(self) -> SafeText | None:
        """Returns an image HTML tag if the topic has an image."""
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" />')
    image_tag.short_description = 'Image'
    
    def get_absolute_url(self) -> str:
        """Returns the URL of the topic."""
        return reverse('quiz:topic', kwargs={'slug': self.slug})
    
    def get_related_topics(self) -> QuerySet:
        """Return queryset of related topics (topics with the same parent as the current topic)."""
        if self.parent:
            return self.parent.get_children().exclude(pk=self.pk)
        else:
            return Topic.objects.filter(parent__isnull=True).exclude(pk=self.pk)
    
    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
        if self.image:
            try:
                target_size = (300, 300)
                img = Image.open(self.image.path)
                img.thumbnail(target_size)
                thumbnail_size = img.size
                new_img = Image.new("RGBA", target_size, (52, 58, 64))
                left = (target_size[0] - thumbnail_size[0]) // 2
                top = (target_size[1] - thumbnail_size[1]) // 2
                new_img.paste(img, (left, top))
                new_img.save(self.image.path, 'PNG')
            except Exception as e:
                print(f"Error processing image: {e}")

    def delete(self, *args, **kwargs) -> None:
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
    
    def get_topic_completion(self, user_id: int) -> float:
        """Calculate a user's completion of the topic."""
        descentants = self.get_descendants(include_self=True)
        user_completions: QuerySet[Completion] = Completion.objects.filter(
            user__id=user_id, 
            quiz__topic__in=descentants, 
        )
        topic_quizzes_completed_count: int = user_completions.count()
        total_topic_quizzes_count: int = Quiz.objects.filter(topic__in=descentants).count()
        
        if total_topic_quizzes_count == 0:
            return 0.0
        
        return (topic_quizzes_completed_count / total_topic_quizzes_count) * 100.0
    
    def get_amount_of_quizzes(self) -> int:
        descentants: QuerySet[Topic] = self.get_descendants(include_self=True)
        total_topic_quizzes_count: int = Quiz.objects.filter(topic__in=descentants).count()
        return total_topic_quizzes_count
    
    def __str__(self) -> str:
        return self.name

class Question(models.Model):
    """
    Represents a question in a quiz.

    Each question belongs to a specific quiz and has a text and complexity level.
    """
    
    COMPLEXITY_CHOICES = (
        ('1', 'Easy'),
        ('2', 'Medium'),
        ('3', 'Hard'),
    )

    quiz = models.ForeignKey(
        to=Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Quiz', 
        help_text='Choose a quiz this question belongs to.'
    )
    text = models.TextField(
        verbose_name='Question Text', 
        max_length=500, 
        editable=True, 
        help_text='Enter the question.'
    )
    complexity = models.CharField( 
        verbose_name='Complexity', 
        max_length=20, 
        choices=COMPLEXITY_CHOICES, 
        default='1',
        help_text='Choose the question complexity from 1 to 3.'
    )

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['quiz']
    
    def has_multiple_answers(self) -> bool:
        """Check if the question has multiple correct answers."""
        return self.answers.filter(is_correct=True).count() > 1
    
    def get_correct_answers(self) -> QuerySet:
        """Return queryset of correct choice answers for the question."""
        return self.answers.filter(is_correct=True)

    def get_incorrect_answers(self) -> QuerySet:
        """Return queryset of incorrect choice answers for the question."""
        return self.answers.filter(is_correct=False)

    def __str__(self) -> str:
        return self.text

class ChoiceAnswer(models.Model):
    """
    Represents a choice answer for a question.

    Each choice answer has it's text, belongs to a specific question and can be marked as correct or incorrect.
    """
    
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Question',
        help_text='Choose the question this answer belongs to.', 
    )
    text = models.CharField(
        verbose_name='Answer Text',
        max_length=255,
        help_text='Enter the answer text.', 
    )
    is_correct = models.BooleanField(
        verbose_name='Is Correct?', 
        default=False, 
        help_text='Mark if this answer is correct or incorrect.', 
    )

    class Meta:
        verbose_name = 'Choice Answer'
        verbose_name_plural = 'Choice Answers'
        ordering = ['question']
    
    def __str__(self) -> str:
        return f'{'Correct' if self.is_correct else 'Incorrect'} - {self.text}'

class Completion(models.Model):
    """
    Represents a completion of a quiz.

    Each completion has the user who made the completion, the quiz being completed and the time of the completion.
    """
    
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        related_name='quiz_completions',
        verbose_name='User', 
        help_text='The user who the completion belongs to.', 
    )
    quiz = models.ForeignKey(
        to=Quiz, 
        on_delete=models.CASCADE,
        related_name='completions',
        verbose_name='Quiz', 
        help_text='The quiz being completed.', 
    )
    percentage = models.FloatField(
        verbose_name='Percentage', 
        help_text='Completion percentage.', 
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    picked_answers = models.ManyToManyField(
        to=ChoiceAnswer, 
        through='PickedAnswer', 
        related_name='completions', 
        verbose_name='Picked Answers', 
        help_text='Answers that user picked from quiz questions.', 
    )
    created_at = models.DateTimeField(
        verbose_name='Created at', 
        auto_now_add=True, 
        help_text='The date and time when the completion was made.', 
    )
    
    class Meta:
        db_table_comment = 'Quiz completions.'
        verbose_name = 'Completion'
        verbose_name_plural = 'Completions'
        ordering = ['quiz']
        unique_together = ['user', 'quiz']
    
    def __str__(self):
        return f'{self.user.username} completed {self.quiz.name} with {self.percentage}%'

class PickedAnswer(models.Model):
    """
    Represents a picked answer in a completed quiz.

    Each PickedAnswer has the completion it was picked in and the answer that was picked.
    """
    
    completion = models.ForeignKey(
        to=Completion, 
        on_delete=models.CASCADE, 
        verbose_name='Completion', 
        help_text='The completion instance that this answer was picked in.', 
    )
    answer = models.ForeignKey(
        to=ChoiceAnswer, 
        on_delete=models.CASCADE, 
        verbose_name='Answer', 
        help_text='The answer that was picked.'
    )
    
    class Meta:
        db_table_comment = 'A picked answer in a completion.'
        verbose_name = 'Picked answer'
        verbose_name_plural = 'Picked answers'
        ordering = ['completion']
    
    def __str__(self):
        return f"{self.completion.user.username} picked {self.answer.text} and was {'correct' if self.answer.is_correct else 'incorrect'}"
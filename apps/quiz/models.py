import uuid

from django.db import models
from django.urls import reverse
from django.utils.safestring import SafeText, mark_safe
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey

from PIL import Image


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
    completions = models.PositiveIntegerField(
        verbose_name='Completions Count', 
        blank=True,
        default=0,
        help_text='Amount of times the quiz has been completed.'
    )
    
    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
        ordering = ['-edited_at', 'topic']
    
    def get_absolute_url(self) -> str:
        """Returns the URL of the quiz."""
        return reverse('quiz:quiz', kwargs={'topic_slug': self.topic.slug, 'slug': self.slug})
    
    # FIXME: Fix finding percentage value for complexity
    # def get_percentage_value_for_complexity(self) -> dict:
    #     total_percentage = 0
    #     amount_of_complexities = {
    #         '1': 0, 
    #         '2': 0, 
    #         '3': 0, 
    #     }
    #     percentage_value_for_complexity = {
    #         '1': 0, 
    #         '2': 0, 
    #         '3': 0, 
    #     }
    #     weights = {
    #         '1': 1, 
    #         '2': 1.5, 
    #         '3': 2, 
    #     }
        
    #     # Find total questions and amount of questions of each complexity
    #     total_questions = self.questions.count()
    #     for complexity in self.questions.all().values_list('complexity', flat=True):
    #         amount_of_complexities[complexity] += 1
    #     assert total_questions == sum(value for value in amount_of_complexities.values()), "Amount of questions in each quantity doesn't equal the total amount."
        
    #     # FIXME: Find percentage value for complexity
    #     for complexity, count in amount_of_complexities.items():
            
    #         # If all questions are of the same complexity
    #         if count == total_questions:
    #             percentage_value_for_complexity[complexity] = 100 / count
    #             total_percentage = 100
    #             break
            
    #         # If there are no questions of such complexity
    #         elif count == 0:
    #             continue
            
    #         percentage_value_for_complexity[complexity] = (count * weights[complexity] / total_questions) * 100
    #         total_percentage += percentage_value_for_complexity[complexity]
        
    #     # Round up percentage values for complexity
    #     percentage_value_for_complexity = {key: round(value, 1) for key, value in percentage_value_for_complexity.items()}
    #     print(percentage_value_for_complexity)
    #     return percentage_value_for_complexity

    def get_percentage_value_for_complexity(self) -> dict:
        total_percentage = 0
        percentage_value_for_complexity = {
            '1': 0, 
            '2': 0, 
            '3': 0, 
        }
        
        total_questions = self.questions.count()

        value = round(100 / total_questions, 1)
        percentage_value_for_complexity = {
            '1': value,
            '2': value,
            '3': value,
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
    
    def save(self, *args, **kwargs):
        if self.image:
            super().save(*args, **kwargs)
            img = Image.open(self.image.path)
            max_size = (450, 300)
            img.thumbnail(max_size)
            img.save(self.image.path)
        super().save(*args, **kwargs)
        
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
    
    # TODO: make a save model check
    # def save(self, *args, **kwargs) -> None:
    #     answers: QuerySet[ChoiceAnswer] = self.answers.all()
    #     if not answers or answers.count() < 2 or not answers.filter(is_correct=True).exists():
    #         return

    #     super().save(*args, **kwargs)
    
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
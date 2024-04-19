from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Author', 
        null=True, 
        default=None, 
    )
    
    title = models.CharField(
        verbose_name='Title', 
        max_length=100, 
        editable=True, 
        help_text='Enter a title for the article.', 
    )
    
    content = models.TextField(
        verbose_name='Content', 
        max_length=1000, 
        blank=True, 
        editable=True, 
        help_text='Enter the content of the article.', 
    )
    
    image = models.ImageField(
        verbose_name='Image', 
        upload_to='article_images',
        help_text='Upload an image for the article.', 
    )
    
    views = models.IntegerField(
        verbose_name='Views', 
        default=0, 
        editable=False, 
        auto_created=True, 
    )
    
    likes = models.PositiveIntegerField(
        verbose_name='Likes', 
        default=0, 
        editable=False, 
        auto_created=True, 
    )
    
    dislikes = models.PositiveIntegerField(
        verbose_name='Dislikes', 
        default = 0, 
        editable = False, 
        auto_created = True, 
    )
    
    created_at = models.DateTimeField(
        verbose_name='Created at', 
        auto_now_add=True, 
    )
    
    edited_at = models.DateTimeField(
        verbose_name='Edited at', 
        auto_now=True, 
    )
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-created_at', 'id']
    
    def __str__(self):
        return f"{self.title} (@{self.author.username})"

class Comment(models.Model):
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name='comments', 
        verbose_name='Article', 
    )
    
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments', 
        verbose_name='Author', 
        null=True, 
        default=None, 
    )
    
    likes = models.PositiveIntegerField(
        verbose_name='Likes', 
        default=0, 
        editable=False, 
        auto_created=True, 
    )
    
    content = models.TextField(
        verbose_name='Content', 
        editable=True, 
        help_text="Enter the content of the comment."
    )
    
    created_at = models.DateTimeField(
        verbose_name='Created at', 
        auto_now_add=True, 
    )
    
    edited_at = models.DateTimeField(
        verbose_name='Edited at', 
        auto_now=True, 
    )
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-likes', '-created_at']
        db_table_comment = 'Article comments'
    
    def __str__(self):
        return f'"{self.content[:20]}..." - @{self.author.username}. ({self.article.title})'
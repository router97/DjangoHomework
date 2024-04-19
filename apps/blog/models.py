from math import ceil

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
        max_length=10000, 
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
    
    def get_reading_time(self):
        word_list = self.content.split()
        word_count = len(word_list)
        reading_time_minutes = word_count / 150
        
        if reading_time_minutes < 1:
            reading_time_seconds = reading_time_minutes * 60
            return f"{ceil(reading_time_seconds)} sec"
        elif reading_time_minutes < 60:
            return f"{ceil(reading_time_minutes)} min"
        else:
            reading_time_hours = reading_time_minutes / 60
            return f"{ceil(reading_time_hours)} hr"
    
    def get_like_dislike_percentage(self):
        
        if self.likes and self.dislikes:
            return int( ( (self.likes - self.dislikes) / (self.likes + self.dislikes) ) * 100 )
        
        if not self.dislikes and self.likes:
            return 100
        
        if self.dislikes and not self.likes or not self.dislikes and not self.likes:
            return 0
    
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
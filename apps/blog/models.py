from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE, related_name='articles', null=True, default=None)
    
    title = models.CharField(verbose_name='Title', max_length=20, editable=True)
    content = models.TextField(verbose_name='Content', blank=True, editable=True)
    
    image = models.ImageField(verbose_name='Image', upload_to='article_images')
    
    views = models.IntegerField(verbose_name='Views', default=0, editable=False, auto_created=True)
    likes = models.IntegerField(verbose_name='Likes', default=0, editable=False, auto_created=True)
    dislikes = models.IntegerField(verbose_name='Dislikes', default = 0, editable = False, auto_created = True)
    
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    edited_at = models.DateTimeField(verbose_name='Edited at', auto_now=True)
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} (@{self.author.username})"

class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name='Article', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE, related_name='comments', null=True, default=None)
    
    likes = models.IntegerField(verbose_name='Likes', default=0, editable=False, auto_created=True)
    content = models.TextField(verbose_name='Content', editable=True)
    
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    edited_at = models.DateTimeField(verbose_name='Edited at', auto_now=True)
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-likes']
    
    def __str__(self):
        return f'"{self.content[:20]}..." - @{self.author.username}. ({self.article.title})'
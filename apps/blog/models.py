from django.db import models

class Article(models.Model):
    title = models.CharField(max_length = 20, verbose_name = 'Title', editable = True)
    content = models.TextField(verbose_name = 'Content', blank = True, editable = True)
    
    image = models.ImageField(verbose_name = 'Image', upload_to='article_images')
    
    views = models.IntegerField(verbose_name = 'Views', default = 0, editable = False, auto_created = True)
    likes = models.IntegerField(verbose_name = 'Likes', default = 0, editable = False, auto_created = True)
    
    created_at = models.DateTimeField(verbose_name = 'Created at', auto_now_add = True)
    edited_at = models.DateTimeField(verbose_name = 'Edited at', auto_now = True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
    
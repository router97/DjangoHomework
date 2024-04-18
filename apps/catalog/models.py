import uuid

from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Catalog(MPTTModel):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        verbose_name='ID', 
    )
    
    name = models.CharField(
        verbose_name='Name', 
        max_length=255, 
        help_text='Enter the name of the category.', 
    )
    
    slug = models.SlugField(
        verbose_name='URL', 
        max_length=255, 
        unique=True, 
        help_text='A unique slug for the category.', 
    )
    
    description = models.TextField(
        verbose_name='Description', 
        blank=True, 
        help_text='Enter a description for the category.', 
    )
    
    image = models.ImageField(
        verbose_name='Image', 
        upload_to='catalog/', 
        blank=True, 
        null=True, 
        help_text='Upload an image for the category.', 
    )
    
    parent = TreeForeignKey(
        to='self', 
        on_delete=models.CASCADE,
        related_name='child',
        blank=True,
        null=True, 
        verbose_name='Parent Category', 
    )
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    def __str__(self):
        return self.name    
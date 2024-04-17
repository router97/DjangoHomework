import uuid

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Catalog(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='Name')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Description')
    image = models.ImageField(verbose_name='Image', upload_to='catalog/', blank=True, null=True)
    parent = TreeForeignKey(
        to='self', 
        on_delete=models.CASCADE,
        related_name='child',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return self.name
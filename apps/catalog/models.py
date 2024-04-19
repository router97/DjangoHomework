import uuid

from django.db import models
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Catalog(MPTTModel):
    id = models.UUIDField(
        verbose_name='ID', 
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
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
        verbose_name='Parent Category', 
        blank=True, 
        null=True, 
    )
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        db_table_comment = 'Product categories'
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(
        verbose_name='ID', 
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
    )
    
    name = models.CharField(
        verbose_name='Name', 
        max_length=255, 
        help_text='Enter the name of the product.', 
    )
    
    slug = models.SlugField(
        verbose_name='URL', 
        max_length=255, 
        unique=True, 
        help_text='A unique slug for the product.', 
    )
    
    description = models.TextField(
        verbose_name='Description', 
        blank=True, 
        null=True, 
        help_text='Enter a description for the product.', 
    )
    
    quantity = models.PositiveIntegerField(
        verbose_name='Quantity', 
        default=0, 
        help_text='Amount available', 
    )
    
    price = models.DecimalField(
        verbose_name='Price', 
        max_digits=10, 
        decimal_places=2, 
    )
    
    created_at = models.DateTimeField(
        verbose_name='Created at', 
        auto_now_add=True, 
    )
    
    updated_at = models.DateTimeField(
        verbose_name='Updated at', 
        auto_now=True, 
    )
    
    image = models.ImageField(
        verbose_name='Image', 
        upload_to='catalog/product/', 
        blank=True, 
        null=True, 
        help_text='Upload an image for the product.', 
    )
    
    category = models.ManyToManyField(
        to=Catalog, 
        through='ProductCategory', 
        related_name='products', 
        verbose_name='Categories', 
        blank=True, 
    )
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['price', 'quantity']
    
    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'category_slug': self.main_category().slug, 'slug': self.slug})
    
    # FIXME: ijfmeakk
    def main_category(self):
        category = self.category.filter(productcategory__is_main=True).first()
        if category:
            return category
        return self.category.first()
    
    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    product = models.ForeignKey(
        to=Product, 
        on_delete=models.CASCADE, 
        verbose_name='Product', 
        help_text='The product associated with this category.'
    )
    
    category = models.ForeignKey(
        to=Catalog, 
        on_delete=models.CASCADE, 
        verbose_name='Category', 
        help_text='The category for this product.'
    )
    
    is_main = models.BooleanField(
        verbose_name='Main Category', 
        default=False, 
        help_text='Shows if the category is the main one for the product.'
    )
    
    class Meta:
        verbose_name = 'Product category'
        verbose_name_plural = 'Product categories'
    
    # FIXME: wefijkfj2
    def save(self, *args, **kwargs):
        if self.is_main:
            ProductCategory.objects.filter(product=self.product, is_main=True).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.product.name} -> {self.category.name}'
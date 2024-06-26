# Generated by Django 5.0.2 on 2024-04-18 07:37

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_catalog_options_alter_catalog_table_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name of the product.', max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(help_text='A unique slug for the product.', max_length=255, unique=True, verbose_name='URL')),
                ('description', models.TextField(blank=True, help_text='Enter a description for the product.', null=True, verbose_name='Description')),
                ('quantity', models.PositiveIntegerField(default=0, help_text='Amount available', verbose_name='Quantity')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_main', models.BooleanField(default=False, verbose_name='Main Category')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.catalog', verbose_name='Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product category',
                'verbose_name_plural': 'product categories',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='products', through='catalog.ProductCategory', to='catalog.catalog', verbose_name='Categories'),
        ),
    ]

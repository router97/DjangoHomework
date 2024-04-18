# Generated by Django 5.0.2 on 2024-04-18 06:18

import django.db.models.deletion
import mptt.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='description',
            field=models.TextField(blank=True, help_text='Enter a description for the catalog.', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='catalog',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='catalog',
            name='image',
            field=models.ImageField(blank=True, help_text='Upload an image for the catalog.', null=True, upload_to='catalog/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='catalog',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='catalog.catalog', verbose_name='Parent Category'),
        ),
        migrations.AlterField(
            model_name='catalog',
            name='slug',
            field=models.SlugField(help_text='A unique slug for the catalog.', max_length=255, unique=True, verbose_name='URL'),
        ),
    ]
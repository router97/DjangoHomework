# Generated by Django 5.0.2 on 2024-03-05 14:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_article_dislikes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField(auto_created=True, default=0, editable=False, verbose_name='Likes')),
                ('author', models.CharField(max_length=20, verbose_name='Author')),
                ('content', models.TextField(blank=True, verbose_name='Content')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('edited_at', models.DateTimeField(auto_now=True, verbose_name='Edited at')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.article', verbose_name='Article')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['likes'],
            },
        ),
    ]

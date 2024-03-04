# Generated by Django 5.0.2 on 2024-03-02 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField(auto_created=True, default=0, editable=False, verbose_name='Likes')),
                ('views', models.IntegerField(auto_created=True, default=0, editable=False, verbose_name='Views')),
                ('title', models.CharField(max_length=20, verbose_name='Title')),
                ('content', models.TextField(blank=True, verbose_name='Content')),
                ('image', models.ImageField(blank=True, upload_to='apps/blog/static/', verbose_name='Image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('edited_at', models.DateTimeField(auto_now=True, verbose_name='Edited at')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'ordering': ['-created_at'],
            },
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]

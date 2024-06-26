# Generated by Django 5.0.2 on 2024-04-24 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_alter_choiceanswer_question_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ['-edited_at', 'topic'], 'verbose_name': 'Quiz', 'verbose_name_plural': 'Quizzes'},
        ),
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=models.TextField(blank=True, help_text='Enter a description of the topic.', max_length=1000, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='short_description',
            field=models.TextField(blank=True, help_text='Enter a short description of the topic.', max_length=100, null=True, verbose_name='Short Description'),
        ),
    ]

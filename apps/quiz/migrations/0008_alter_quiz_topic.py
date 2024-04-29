# Generated by Django 5.0.2 on 2024-04-26 22:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_quiz_completions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='topic',
            field=models.ForeignKey(help_text='Choose the topic of the quiz.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='quiz.topic', verbose_name='Topic'),
        ),
    ]

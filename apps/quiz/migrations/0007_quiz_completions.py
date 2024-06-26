# Generated by Django 5.0.2 on 2024-04-26 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_alter_quiz_options_alter_topic_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='completions',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='Amount of times the quiz has been completed.', verbose_name='Completions Count'),
        ),
    ]

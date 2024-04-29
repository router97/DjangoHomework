# Generated by Django 5.0.2 on 2024-04-23 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_remove_question_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='complexity',
            field=models.CharField(choices=[('1', 'Easy'), ('2', 'Medium'), ('3', 'Hard')], default='1', help_text='Choose the question complexity from 1 to 3.', max_length=20),
        ),
    ]

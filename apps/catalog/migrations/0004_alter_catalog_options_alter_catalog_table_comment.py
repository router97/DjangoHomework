# Generated by Django 5.0.2 on 2024-04-18 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_catalog_description_alter_catalog_image_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='catalog',
            options={'ordering': ['name'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelTableComment(
            name='catalog',
            table_comment='Product categories',
        ),
    ]

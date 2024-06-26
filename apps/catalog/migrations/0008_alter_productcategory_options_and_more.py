# Generated by Django 5.0.2 on 2024-04-19 07:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': 'Product category', 'verbose_name_plural': 'Product categories'},
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='category',
            field=models.ForeignKey(help_text='The category for this product.', on_delete=django.db.models.deletion.CASCADE, to='catalog.catalog', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='is_main',
            field=models.BooleanField(default=False, help_text='Shows if the category is the main one for the product.', verbose_name='Main Category'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='product',
            field=models.ForeignKey(help_text='The product associated with this category.', on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Product'),
        ),
    ]

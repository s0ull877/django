# Generated by Django 5.0.6 on 2024-05-12 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_product_sale_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(default=[1], to='goods.category'),
        ),
    ]

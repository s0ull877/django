# Generated by Django 5.1.2 on 2024-10-17 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redirect', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='redirectmodel',
            name='redirect_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Число редиректов'),
        ),
    ]

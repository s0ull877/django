# Generated by Django 5.1 on 2024-09-23 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Подтверждено'),
        ),
    ]

# Generated by Django 5.1 on 2024-09-20 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='created_at',
            new_name='date',
        ),
    ]

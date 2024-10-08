# Generated by Django 5.1 on 2024-09-19 20:21

import users.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=users.utils.user_avatar_upload),
        ),
    ]

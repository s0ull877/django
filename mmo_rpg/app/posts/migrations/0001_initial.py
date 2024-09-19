# Generated by Django 5.1 on 2024-09-19 20:55

import django.db.models.deletion
import posts.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='описание под постом')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('liked_users', models.ManyToManyField(blank=True, related_name='liked_users', to=settings.AUTH_USER_MODEL, verbose_name='Лайкнувшие пользователи')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец поста')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.postcategory', verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('status', models.BooleanField(blank=True, null=True, verbose_name='Подтверждено')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец комментария')),
                ('to_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post', verbose_name='Прокоментированный пост')),
            ],
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=posts.utils.custom_upload)),
                ('to_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post', verbose_name='Фото к публикации')),
            ],
        ),
    ]

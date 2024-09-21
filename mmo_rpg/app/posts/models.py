from typing import Iterable
from django.db import models
from users.models import User

from .utils import custom_upload


class PostCategory(models.Model):

    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'
    

class Post(models.Model):

    owner = models.ForeignKey(
        verbose_name='Владелец поста',
        on_delete=models.CASCADE,
        to=User)
    text = models.TextField(
        verbose_name='описание под постом')
    category=models.ForeignKey(
        verbose_name='Категория',
        on_delete=models.CASCADE,
        to=PostCategory)
    created_at=models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)
    liked_users=models.ManyToManyField(
        related_name='liked_users',
        verbose_name='Лайкнувшие пользователи',
        to=User, blank=True)
    
    def __str__(self) -> str:

        return f'{self.owner.username} | {self.created_at}'



class PostImage(models.Model):

    to_post=models.ForeignKey(
        verbose_name='Фото к публикации',
        on_delete=models.CASCADE,
        to=Post)
    image=models.ImageField(upload_to=custom_upload)

    def __str__(self) -> str:
        return f'Фото к посту {self.to_post}'

class Notification(models.Model):

    owner=models.ForeignKey(
        verbose_name='Владелец комментария',
        on_delete=models.CASCADE,
        to=User)
    to_post=models.ForeignKey(
        verbose_name='Прокоментированный пост',
        on_delete=models.CASCADE,
        to=Post)
    created_at=models.DateTimeField(
        verbose_name='Дата публикации',
        name='date',
        auto_now_add=True)
    text=models.TextField(
        verbose_name='Текст комментария')
    status=models.BooleanField(
        verbose_name='Подтверждено',
        null=True,blank=True)
    
    def __str__(self) -> str:
        return f'Комментарий {self.owner.username} от {self.date} к {self.to_post}'
    
    def save(self, *args, **kwargs) -> None:

        if self.owner == self.to_post.owner:

            self.status=True

        if self.status is False:
            
            self.delete()
            return

        return super().save(*args, **kwargs)
from django.db import models
from users.models import User

from .utils import custom_upload

class Post(models.Model):

    owner = models.ForeignKey(
        verbose_name='Владелец поста',
        on_delete=models.CASCADE,
        to=User)
    text = models.TextField(
        verbose_name='описание под постом')
    created_at=models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)
    
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
        auto_now_add=True)
    text=models.TextField(
        verbose_name='Текст комментария')
    status=models.BooleanField(
        verbose_name='Подтверждено',
        null=True,blank=True)
    
    def __str__(self) -> str:
        return f'Комментарий {self.owner.username} от {self.created_at} к {self.to_post}'
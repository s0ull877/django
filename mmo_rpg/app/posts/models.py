import os
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
        verbose_name='Описание под постом')
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

        return f'{self.owner.username} | {self.id}'



class PostImage(models.Model):

    to_post=models.ForeignKey(
        verbose_name='Фото к публикации',
        on_delete=models.CASCADE,
        to=Post)
    image=models.ImageField(upload_to=custom_upload, 
                            blank=False, null=False)

    def __str__(self) -> str:
        return f'Фото к посту {self.to_post}'
    
    
    # TODO это работает только на 1 обьект, не на bulk
    def delete(self, using=None, keep_parents=False):

        os.remove(self.image.path)

        return super(PostImage, self).delete(using, keep_parents)


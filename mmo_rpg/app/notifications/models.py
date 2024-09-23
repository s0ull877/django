from django.db import models

from users.models import User
from posts.models import Post

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
        default=None,
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

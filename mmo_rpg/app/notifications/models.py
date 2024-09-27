from typing import Iterable
from django.conf import settings
from django.core.mail import send_mail
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
    

class EmailNotification(models.Model):

    to=models.ForeignKey( 
        verbose_name='Кому отправить',
        to=User, on_delete=models.SET_NULL, 
        blank=True, null=True)
    title = models.CharField(
        verbose_name='Заголовок сообщения',
        default='Новое уведомление от Axevich')
    message=models.TextField(
        verbose_name='Тело сообщения')
    created_at=models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True)
    # Если автоматически то раз в месяц удаляются такие сообщения
    manual=models.BooleanField(
        verbose_name='Создано автоматически',)
    

    def send_email(self):

        if self.to is None:

            recipient_list = User.objects.values_list('email', flat=True)

        else:
            recipient_list = [self.to.email]


        send_mail(
            subject=self.title,
            message=self.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
            )


    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        ):

        super().save(*args, force_insert, force_update, using, update_fields)
        
        self.send_email()
        

    def __str__(self) -> str:
        
        name = self.to if self.to is not None else 'Всем пользователям'

        return f'Рассылка от {self.created_at} | {self.to}'
        



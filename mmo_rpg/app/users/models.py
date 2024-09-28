from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.urls import reverse
from django.utils.timezone import now
from .utils import user_avatar_upload


class User(AbstractUser):

    last_name = None
    username = models.CharField(
        max_length=20, unique=True)
    image = models.ImageField(
        upload_to=user_avatar_upload, #кастомный upload
        null=True, blank=True)
    status = models.TextField(
        verbose_name='Статус пользователя', 
        max_length=128, blank=True, 
        null=True, default=None)
    email = models.EmailField(
        verbose_name="email address", 
        blank=False, unique=True)
    is_verified_email = models.BooleanField(
        default=False)

    # для менеджмента, команды для создания root`a в докер контейнере
    def create_superser(self, username:str, email:str, password:str ):
        self.objects.save(
            username=username, email=email, password=password, 
            is_verified_email=True, is_staff=True, is_superuser=True
            )
        

class EmailVerification(models.Model):

    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()


    def __str__(self):
        return f'EmailVerification for {self.user.email}'
    

    def send_verification_email(self):

        # ссылка для пользователя для верификации
        link = reverse('users:verify', kwargs={'email': self.user.email, 'code': self.code})
        verify_link = f'{settings.HOSTNAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи по почте {} перейдите по ссылке: {}'.format(
            self.user.email,
            verify_link
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
            )

    
    # не просрочена ли ссылка
    def is_expired(self):
        
        return now() >= self.expiration
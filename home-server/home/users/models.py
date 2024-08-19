from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.models import AbstractUser

from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    
    email = models.EmailField(_("email address"), blank=True, unique=True)
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    is_verified = models.BooleanField(default=False)


class EmailVerification(models.Model):

    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'EmailVerification for {self.user.username}'
    
    def is_expired(self):
        return now() >= self.expiration
    
    def send_verification_email(self):
        
        link = reverse('users:verify', kwargs={'email': self.user.email, 'code': self.code})
        verification_url = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Спасибо за регистрацию на сайте {}!\n\
            Для подтверждения учетной записи для {} перейдите по ссылке: {}.\n\
            Ссылка активна первые 15 минут после отправки сообщения.'.format(
            settings.DOMAIN_NAME,
            self.user.username,
            verification_url
        )

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.user.email],
            fail_silently=False,
        )


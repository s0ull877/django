from django.db import models
from django.contrib.auth.models import AbstractUser

from .utils import user_avatar_upload

class User(AbstractUser):

    last_name = None
    username = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to=user_avatar_upload, null=True, blank=True)
    status = models.TextField(verbose_name='Статус пользователя', max_length=128, blank=True, null=True, default=None)
    is_verified_email = models.BooleanField(default=False)

    def create_superser(self, username:str, email:str, password:str ):
        self.objects.save(
            username=username, email=email, password=password, \
            is_verified_email=True, is_staff=True, is_superuser=True
            )
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)

    def create_superser(self, username:str, email:str, password:str ):
        self.objects.save(
            username=username, email=email, password=password, \
            is_verified_email=True, is_staff=True, is_superuser=True
            )

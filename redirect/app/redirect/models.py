from django.db import models
from django.conf import settings

class RedirectModel(models.Model):

    path = models.CharField(
        verbose_name='Путь редиректа',
        unique=True,
        max_length=10
    )
    redirect_to = models.URLField(
        verbose_name='Редирект на'
    )

    def __str__(self):
        
        return f'{self.id} | {self.path}'


    def get_redirect_uri(self):

        return f'{settings.SITE_URL}/{self.path}'
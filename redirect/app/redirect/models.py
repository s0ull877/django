from django.db import models

class RecirectModel(models.Model):

    path = models.CharField(
        verbose_name='Путь редиректа',
        unique=True
    )
    redirect_to = models.URLField(
        verbose_name='Редирект на'
    )

    def __str__(self):
        
        return f'{self.id} | {self.path}'

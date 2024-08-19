from django.db import models

class Link(models.Model):

    name = models.CharField(
        verbose_name='Название',
        max_length=60
        )
    telegram_link = models.CharField(
        verbose_name='Ссылка',
        max_length=70,
        unique=True
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
        )
    
    class Meta:

        verbose_name='Link'
        verbose_name_plural='Ссылки'

    def __str__(self):
        return self.name
    
   
    

class Worker(models.Model):

    worker_tg_id=models.CharField(
        max_length=30,
        verbose_name='Telegram ID',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Полное имя',
        )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=20
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:

        verbose_name='Аккаунт'
        verbose_name_plural='Аккаунты'

    def __str__(self) -> str:
        return self.name
    

class Sub(models.Model):

    link = models.ForeignKey(
        to=Link, 
        on_delete=models.CASCADE, 
        verbose_name='Ссылка'
        )
    worker = models.ForeignKey(
        to=Worker, 
        on_delete=models.SET_NULL, null=True, 
        verbose_name='Аккаунт'
                               )
    created = models.DateTimeField(
        verbose_name='Дата подписки'
    )

    class Meta:

        verbose_name='Подписчик'
        verbose_name_plural='Подписчики'

    def __str__(self) -> str:
        return f'{self.worker} -> {self.link}'

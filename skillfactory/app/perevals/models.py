from django.db import models

from users.models import User


class Coordinates(models.Model):

    latitude=models.FloatField(verbose_name='Широта')
    longitude=models.FloatField(verbose_name='Длина')
    height=models.IntegerField(verbose_name='Высота')

    def __str__(self) -> str:
        return f'{self.latitude} {self.longitude} {self.height}'


class Pereval(models.Model):

    created_at=models.DateTimeField(
        verbose_name='Дата создания',
        name='date_added',
        auto_now_add=True
    )
    beautyTitle=models.CharField(
        verbose_name='Загаловок'
    )
    title=models.CharField(
        verbose_name='Название'
    )
    other_title=models.CharField(
        verbose_name='Доп. название'
    )
    connect=models.CharField()
    add_time=models.DateTimeField(
        verbose_name='Дата добавления пользователем'
    )
    user = models.ForeignKey(
        to=User,
        verbose_name='Добавлено пользователем'
    )
    winter_level=models.CharField(
        verbose_name="Тяжесть пути зимой", 
        max_length=2, 
        blank=True, null=True)
    summer_level=models.CharField(
        verbose_name="Тяжесть пути летом", 
        max_length=2,
        blank=True, null=True)
    autumn_level=models.CharField(
        verbose_name="Тяжесть пути осенью", 
        max_length=2,
        blank=True, null=True)
    spring_level=models.CharField(
        verbose_name="Тяжесть пути весной", 
        max_length=2,
        blank=True, null=True)
    

    def __str__(self) -> str:
        return f'{self.beautyTitle} {self.title} | {self.user}'

    class Meta:

        db_table = 'pereval_added'


class PerevalImage(models):

    to_pereval=models.ManyToManyField(
        to=Pereval,
        verbose_name='Фото к перевалу')
    title=models.CharField(
        verbose_name='Описание к фотографии')
    image = models.ImageField(
        verbose_name='Изображение')
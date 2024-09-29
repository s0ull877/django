from django.db import models

from users.models import User


class Coordinates(models.Model):

    latitude=models.FloatField(verbose_name='Широта')
    longitude=models.FloatField(verbose_name='Длина')
    height=models.IntegerField(verbose_name='Высота')

    def __str__(self) -> str:
        return f'{self.latitude} {self.longitude} {self.height}'
    

class PerevalLevel(models.Model):

    CHOICES=(
        ('1A', '1А'),
        ('1B', '1Б'),
        ('2A', '2А'),
        ('2B', '2Б'),
        ('3A', '3А'),
        ('3B', '3Б'),
    )

    winter=models.CharField(
        verbose_name='Зимой',
        choices=CHOICES,
        blank=True, null=True)
    summer=models.CharField(
        verbose_name='Летом',
        choices=CHOICES,
        blank=True, null=True)
    autumn=models.CharField(
        verbose_name='Осенью',
        choices=CHOICES,
        blank=True, null=True)
    spring=models.CharField(
        verbose_name='Весной',
        choices=CHOICES,
        blank=True, null=True)


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
        to=User, on_delete=models.CASCADE,
        verbose_name='Добавлено пользователем'
    )
    level=models.OneToOneField(
        verbose_name='Уровень сложности',
        to=PerevalLevel, on_delete=models.PROTECT
    )
    coordinates=models.OneToOneField(
        verbose_name='Координаты перевала',
        to=Coordinates, on_delete=models.PROTECT)

    # изображения досавать prefetchem

    def __str__(self) -> str:
        return f'{self.beautyTitle} {self.title} | {self.user}'

    class Meta:

        db_table = 'pereval_added'


class PerevalImage(models):

    to_pereval=models.ForeignKey(
        to=Pereval, on_delete=models.CASCADE,
        verbose_name='Фото к перевалу')
    title=models.CharField(
        verbose_name='Описание к фотографии')
    image = models.ImageField(
        verbose_name='Изображение')
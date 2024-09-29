from django.db import models

class User(models.Model):

    email=models.EmailField(
        verbose_name='Эл. почта',
        unique=True)
    fam = models.CharField(
        verbose_name='Фамилия пользователя')
    name = models.CharField(
        verbose_name='Имя пользователя')
    oct = models.CharField(
        verbose_name='Отчество пользователя')
    phone=models.CharField(
        verbose_name='Номер телефона', 
        max_length=15)


    def full_name(self):

        return f'{self.name} {self.fam} {self.otc}'
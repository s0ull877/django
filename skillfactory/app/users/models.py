from django.db import models

class User(models.Model):

    name = models.CharField(
        verbose_name='Имя пользователя')
    fam = models.CharField(
        verbose_name='Фамилия пользователя')
    oct = models.CharField(
        verbose_name='Отчество пользователя')
    phone=models.CharField(
        verbose_name='Номер телефона', 
        max_length=15)
    email=models.EmailField(
        verbose_name='Эл. почта',
        unique=True)


    def full_name(self):

        return f'{self.name} {self.fam} {self.otc}'
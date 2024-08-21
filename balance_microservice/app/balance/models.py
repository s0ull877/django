from django.db import models

class UserBallance(models.Model):

    user_id=models.PositiveBigIntegerField(
        verbose_name='ID пользователя',
        unique=True
    )

    ballance=models.DecimalField(
        verbose_name='Балланс руб.',
        max_digits=7,
        decimal_places=2
    )

    class Meta:

        verbose_name='Баланс пользователя'
        verbose_name_plural='Балансы пользователей'



    def __str__(self):

        return f'{self.user_id} | {self.ballance}'
    

class BallanceTransaction(models.Model):
    
    user_ballance=models.ForeignKey(
        verbose_name='Баланса Пользователя',
        to=UserBallance, on_delete=models.CASCADE
        )
    
    quantity=models.DecimalField(
        verbose_name='Списание/пополнение',
        max_digits=6,
        decimal_places=2
    )

    created_at=models.DateTimeField(
        verbose_name='Дата',
        auto_now_add=True
    )

    # Откуда были начислены/списаны средства с баланса
    service=models.CharField(
        verbose_name='Сервис пополнения/списания',
        max_length=128    
    )

    description=models.TextField(
        verbose_name='Описание транзакции'
    )


    
from django.db import models

from users.models import User
from products.models import Basket

class Order(models.Model):
    
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3

    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=254)
    price = models.DecimalField(max_digits=11, decimal_places=2, default=1)

    basket_history = models.JSONField(default=dict)
    create = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(default=CREATED, choices=STATUSES)

    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order #{self.id}. {self.first_name} {self.last_name}'


    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.price = baskets.total_sum()
        self.status = self.PAID
        self.basket_history = {
            'purchsed_items': [basket.de_json() for basket in baskets],
        }

        self.save()
        baskets.delete()
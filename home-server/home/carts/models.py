from django.db import models

from users.models import User
from goods.models import Products

class HomeCartQuerySet(models.QuerySet):

    def total_price(self):

        return sum( cart.price for cart in self)
    

    def total_quantity(self):

        return sum(cart.quantity for cart in self)


class HomeCart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    session_key = models.CharField(max_length=32 ,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = HomeCartQuerySet.as_manager()


    class Meta:

        verbose_name= 'Basket'
        verbose_name_plural = 'Baskets'


    def __str__(self):
        
        if self.user:
            return f'Basket for {self.user.username} | Product id - {self.product.id} | Q - {self.quantity}'
    
        return f'Basket for anonym | Product id - {self.product.id} | Q - {self.quantity}'

    
    
    @property
    def price(self):
        return round(self.product.with_discount() * self.quantity, 2)
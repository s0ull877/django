from django.db import models

from users.models import User
from goods.models import Products


class OrderItemQuerySet(models.QuerySet):

    def total_price(self):

        return sum(order.product_price() for order in self)
    
    def total_quantity(self):

        return sum(order.quantity for order in self)
    

class Order(models.Model):

    CREATED = 0
    ON_WAY = 1
    DELIVERED = 2
    RECEIVED = 3

    STATUSES = (
        (CREATED, 'In processing'),
        (ON_WAY, 'On way'),
        (DELIVERED, 'Delivered'),
        (RECEIVED,'Received'),
    )

    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Order owner')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date of create')
    phone_number = models.CharField(max_length=20, default=False, verbose_name='Phone number')
    requires_delivery = models.BooleanField(verbose_name='Delivery')
    delivery_address = models.TextField(null=True, blank=True, verbose_name='Delivery address')
    payment_on_get = models.BooleanField(default=False, verbose_name='Pay on get')
    is_paid = models.BooleanField(default=False, verbose_name='Order is paid')
    status = models.PositiveSmallIntegerField(default=CREATED, choices=STATUSES, verbose_name='Order status')


    class Meta:

        verbose_name_plural = 'Orders'


    def __str__(self) -> str:
        return f'Order №{self.pk} | Purchaser - {self.user.username}'

    
class OrderItem(models.Model):

    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='Order')
    product = models.ForeignKey(to=Products, null=True, on_delete=models.SET_NULL, verbose_name='Product')
    name = models.CharField(max_length=150, verbose_name='Product name')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date of create')

    objects = OrderItemQuerySet.as_manager()


    class Meta:

        verbose_name = 'Sold item'
        verbose_name_plural = 'Sold items'
    
    def __str__(self) -> str:
        return f"Order №{self.order.pk} | Product - {self.product.name}"

    
    def product_price(self):
        return round(self.price * self.quantity, 2)
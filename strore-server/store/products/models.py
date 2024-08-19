from django.db import models

from users.models import User


# Create your models here.
# models = таблицы
class ProductCategory(models.Model):

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name


    class Meta:
        
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'



class Product(models.Model):
    
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images', blank=True, null=True, default=None)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)


    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category}'


    class Meta:

        verbose_name = 'Product'
        verbose_name_plural = 'Products'



class BasketQuerySet(models.QuerySet):


    def total_sum(self):
        return sum(basket.sum() for basket in self)


    def total_quantity(self):
        return sum(basket.quantity for basket in self)



class Basket(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()


    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'


    def sum(self):
        return self.product.price * self.quantity



    def de_json(self):

        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }

        return basket_item

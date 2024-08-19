from django.db import models
from django.urls import reverse

class Categories(models.Model):

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:

        return f'Категория : {self.name}'


class Products(models.Model):

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='goods_image', blank=True, null=True)
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Discount in %')
    quantity = models.PositiveIntegerField(default=0)
    category = models.ManyToManyField(to=Categories, default=[4])

    class Meta:
        db_table = 'product'
        verbose_name = 'product'
        verbose_name_plural = 'products'


    def __str__(self) -> str:

        return f'{self.name} | Кол-во: {self.quantity}'
    

    def get_absolute_url(self):
        return reverse("goods:product", kwargs={"pk": self.pk})

    
    def with_discount(self):

        return round(self.price - (self.price * self.discount) / 100, 2)
    

    def display_id(self):

        return f'{self.id:05}'
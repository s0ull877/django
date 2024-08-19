from django.db import models

class Category(models.Model):

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
    categories = models.ManyToManyField(to=Category, default=[1])
    sale_percent = models.PositiveSmallIntegerField(verbose_name='Sale percent', default=0)


    def __str__(self):
        return f'{self.name}'


    class Meta:

        verbose_name = 'Product'
        verbose_name_plural = 'Products'
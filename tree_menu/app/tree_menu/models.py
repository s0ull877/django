from django.db import models

class Category(models.Model):

    name = models.CharField(verbose_name='Название', max_length=60, unique=True)
    description = models.TextField(verbose_name='Описание', max_length=150, blank=True, null=True)

    class Meta:
        
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
    

class SubCategory(models.Model):

    name = models.CharField(verbose_name='Название', max_length=60, unique=True)
    description = models.TextField(verbose_name='Описание', max_length=150, blank=True, null=True)    
    url = models.URLField(verbose_name='URL ресурса пункта меню', max_length=60, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_item')

    class Meta:
        
        ordering = ('id',)
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


    def __str__(self):
        parent = self.parent if self.parent else f' {self.category.name} |'
        return f'{self.name} <- {parent}'
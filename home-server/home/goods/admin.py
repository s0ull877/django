from django.contrib import admin

# Register your models here.
from goods.models import Categories, Products


# admin.site.register(Categories)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):

    list_display = ['name', 'quantity', 'price', 'discount']
    list_editable = ['quantity','discount']
    search_fields = ['id','name']
    list_filter = ['discount','category']
    fields = [
        'name',
        'category',
        'description',
        'image',
        ('price', 'discount'),
        'quantity',
    ]

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):

    list_display = ['name', 'id']
    prepopulated_fields = {'slug': ('name',)}
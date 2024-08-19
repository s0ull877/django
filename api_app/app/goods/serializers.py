from rest_framework import serializers, fields

from goods.models import Category, Product


class CategorySearializer(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields=('id', 'name', 'description')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'image', 'categories', 'sale_percent')

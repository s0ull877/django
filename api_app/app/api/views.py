from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response

from goods.models import Product, Category
from goods.serializers import ProductSerializer, CategorySearializer


class ProductModelViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):

        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)

        return super(ProductModelViewSet,self).get_permissions()


    def get_queryset(self):

        queryset =  super().get_queryset()

        category_id = self.request.query_params.get('category')
        if category_id:
            return queryset.filter(categories__in=category_id)
        
        return queryset.all()
    


class CategoryModelViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySearializer

    def get_permissions(self):

        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)

        return super(CategoryModelViewSet,self).get_permissions()
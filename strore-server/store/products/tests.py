from django.test import TestCase
from django.urls import reverse
from django import setup

from products.models import Product, ProductCategory

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
setup()


# Create your tests here.

class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse("index") #http://localhost:8000/
        response = self.client.get(path=path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['title'], 'Store')
        # self.assertTemplateUsed(response, 'products\index.html')


class ProductsListViewCase(TestCase):

    fixtures = ['categories.json', 'products.json']

    def setUp(self):
        self.products = Product.objects.all()


    def test_list(self):
        
        path = reverse('products:index')

        response = self.client.get(path=path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        # self.assertTemplateUsed(response, 'products/')
        self.assertEqual(list(response.context_data['object_list']), list(products[:3]))


    def test_list_category(self):
        
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': 1})
        
        response = self.client.get(path=path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertEqual(
                    list(response.context_data['object_list']),
                    list(products.filter(category_id= category.id)[:3])
                )


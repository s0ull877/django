from django.urls import path

from orders.views import create_order

app_name = 'orders'

urlpatterns = [
    path('order-create/', create_order, name='create'),
]

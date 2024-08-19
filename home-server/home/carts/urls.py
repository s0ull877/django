from django.urls import path

from carts.views import basket_add_item, basket_change, basket_delete_item

app_name = 'carts'

urlpatterns = [
    path('basket_add/', basket_add_item, name='add'),
    path('basket_delete/', basket_delete_item, name='delete'),
    path('basket_change/', basket_change, name='change'),
]

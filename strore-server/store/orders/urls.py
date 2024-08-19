
from django.urls import path

from orders.views import OrderCreateViews, OrderSuccess, OrdersListView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('order_create/', OrderCreateViews.as_view(), name='order_create'),
    path('order_success/', OrderSuccess.as_view(), name='succeeded'),
    path('', OrdersListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_list'),
]

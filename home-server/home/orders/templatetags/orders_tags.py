from django import template
from django.db.models import Prefetch

from orders.models import Order, OrderItem

register = template.Library()

@register.simple_tag()
def user_orders(request):
    
    return Order.objects.filter(user=request.user).prefetch_related(Prefetch(
        'orderitem_set',
        queryset=OrderItem.objects.select_related('product')
        )).order_by('-created')


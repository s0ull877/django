from django.contrib import admin

from orders.models import Order

@admin.register(Order)
class Order(admin.ModelAdmin):

    list_display = ('__str__', 'status')
    fields = ('id', 'create', 'price',
        ('first_name', 'last_name'),
        ('email', 'address'),
        'basket_history', 'status', 'initiator',
    )
    readonly_fields = ('id', 'create', 'price',)

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from orders.models import Order, OrderItem
from goods.models import Products



class OrderAdminTab(admin.TabularInline):
    
    model=Order
    fields = (        
        'created',
        'status',
        'payment_on_get',
        'is_paid',
        )
    readonly_fields = ('id', 'created')
    search_fields = ('id',)
    extra=0

    

class OrderItemAdminTab(admin.TabularInline):
    
    model=OrderItem
    fields = ('product', 'name', 'quantity', 'price',)
    search_fields = ('product', 'name',)
    readonly_fields = ('id', 'created')
    extra=0



class ProductIDListFilter(admin.SimpleListFilter):

    title = _("Product ID")

    parameter_name = "product_id"

    def lookups(self, request, model_admin):

        products = Products.objects.all().order_by('id')
        return [(str(product.id), _(str(product.id))) for product in products]

    def queryset(self, request, queryset):
        
        if not self.value():
            return queryset
        
        product_id = self.value()
        queryset = queryset.filter(product__id__exact=product_id)
        return queryset

        
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = ('id_display', 'name', 'created',)
    list_filter = ('order__id','created', 'product__name',ProductIDListFilter,)
    search_fields = ('id',)
    fields = (
        'order',
        'product',
        'name',
        ('price', 'quantity',),
        'created',
        )

    readonly_fields = ('order', 'product', 'name', 'price', 'quantity', 'created',)

    def id_display(self, obj):
        return f'Order №{obj.order.id}'
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display=(
        'id_display',
        'user',
        'payment_on_get',
        'is_paid',
        'created',
        'status'
    )
    search_fields = ('id',)
    readonly_fields = ('id', 'created')
    list_filter = ('requires_delivery', 'status', 'payment_on_get', 'is_paid',)
    inlines = (OrderItemAdminTab,)

    
    def id_display(self, obj):
        return f'Order №{obj.id}'
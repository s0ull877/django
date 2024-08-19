from django.contrib import admin

from carts.models import HomeCart


class CartTabAdmin(admin.TabularInline):

    model=HomeCart
    fields = ['product', 'quantity', 'created']
    search_fields = ['product', 'quantity', 'created']
    readonly_fields = ['created']
    extra = 1


@admin.register(HomeCart)
class HomeCartAdmin(admin.ModelAdmin):

    list_display = ['user_display', 'product_display', 'quantity', 'created']
    list_filter = ['created', 'product__name', 'user']


    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return 'Anonim_user'
    

    def product_display(self, obj):
        return str(obj.product.name)

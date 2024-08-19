from django.contrib import admin

from orders.admin import OrderAdminTab
from users.models import User, EmailVerification
from carts.admin import CartTabAdmin

admin.site.register(EmailVerification)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ['username', 'email','is_verified']
    list_editable = ['is_verified']
    search_fields = ['id','username']
    list_filter = ['is_verified','is_staff']
    fields = [
        'username',
        ('is_active','is_verified','is_staff'),
        ('first_name','last_name'),
        'email',
        'groups',
        'user_permissions',
        'image',
        'date_joined'
    ]

    readonly_fields = ['username', 'email', 'date_joined']

    inlines = [CartTabAdmin,OrderAdminTab]


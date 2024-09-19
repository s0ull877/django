from django.contrib import admin

from .models import Post,PostImage,Notification,PostCategory
# Register your models here.
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Notification)
admin.site.register(PostCategory)
from django.contrib import admin

from .models import Post,PostImage,PostCategory
# Register your models here.
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(PostCategory)
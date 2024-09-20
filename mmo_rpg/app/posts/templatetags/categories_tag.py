from django import template
from django.core.cache import cache

from posts.models import PostCategory

register = template.Library()

@register.simple_tag()
def categories_tag():
        
        # categories = cache.get('categories')

        # if not categories:

        #     categories = PostCategory.objects.all() 
        #     cache.set('categories',  categories, 180)
        #     return categories

        # else:
        #     return categories
        

    categories = PostCategory.objects.all() 
    return categories
    
from django import template
from django.core.cache import cache

from goods.models import Categories

register = template.Library()

@register.simple_tag()
def categories_tag():
        
        categories = cache.get('categories')

        if not categories:

            categories = Categories.objects.all() 
            cache.set('categories',  categories, 60)
            return categories

        else:
            return categories

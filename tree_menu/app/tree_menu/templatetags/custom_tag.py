from django import template
from django.core.exceptions import ObjectDoesNotExist

from tree_menu.models import SubCategory

register = template.Library()

@register.inclusion_tag('tree_menu/menu.html')
def draw_menu(category_name: str = None, subcategory_name: str = None):

    def get_menu(category_name: str = None, category_childrens: list = None):

        # получаем дочерние подкатегории
        categories = list(subcategories.filter(parent=None)) if not category_name \
            else list(subcategories.filter(parent__name=category_name))
        
        try:

            # пытаемся засунуть детей категории, после самого списка, таким образом они отрендарятся как подкатегории в шаблоне
            categories.insert(categories.index(category_childrens[0].parent) + 1, category_childrens)

        except (TypeError, IndexError):

            # TypeError, если subcategory_childrens is None
            # IndexError если subcategory_childrens == []
            pass

        try:

            # дальше идем с низу вверх по глубине, для получения полного списка и последующей корректной отрисовки 
            return get_menu(subcategories.get(name=category_name).parent.name, categories)
        
        except AttributeError:
            # ласт шаг, для инсерта всех подклассов в корень с models.Category
            return get_menu(category_childrens=categories)
        
        except ObjectDoesNotExist:
            # выход из рекурсии, при category_name = None
            return categories


    # Получаем все подкатегории выбранной категории
    subcategories = SubCategory.objects.filter(category__name=category_name)

    # if category_name == subcategory_name, значит на вход пришло models.Category поэтому работаем из корня дерева
    return {'categories': get_menu()} if category_name == subcategory_name else { 'categories': get_menu(subcategory_name)}

# categories это список из списков обьектов Subcategory и\или обьектов Subcategory
# Чтобы построить дерево, нужно правильно сформировать список categories для последующей итерации
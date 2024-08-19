from django.shortcuts import redirect, render

from tree_menu.models import Category

def index(request):
    return redirect('main_menu')

def menu(request):
    return render(request, 'tree_menu/index.html', {'categories': Category.objects.all()})


def draw_menu(request, path):
    splitted_path = path.split('/')
    assert len(splitted_path) > 0, ('= Draw_menu function failed =')
    print(splitted_path)
    return render(
        request, 'tree_menu/index.html', {'category_name': splitted_path[0], 'subcategory_name': splitted_path[-1]})
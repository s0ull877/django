from django.urls import path

from tree_menu.views import draw_menu, index, menu

urlpatterns = [
    path('', menu, name='main_menu'),
    path('<path:path>/', draw_menu, name='draw_menu'),
]
from django.urls import path

from .views import redirect_view

urlpatterns = [
    path('<str:path>/', redirect_view),
]

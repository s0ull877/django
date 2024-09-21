from django.urls import path

from . import views
app_name = 'notifications'

urlpatterns = [
    path('', views.notifications_view, name='notifications'),
    path('', views.change_view, name='change'),
]
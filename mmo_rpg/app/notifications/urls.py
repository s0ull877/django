from django.urls import path

from . import views
app_name = 'notifications'

urlpatterns = [
    path('', views.notifications_view, name='notifications'),
    path('change/', views.change_view, name='change'),
    path('like/<int:pk>', views.like_view, name='like'),
]
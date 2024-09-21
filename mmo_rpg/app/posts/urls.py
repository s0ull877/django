from django.urls import path

from . import views
app_name = 'posts'

urlpatterns = [
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('post/<int:pk>', views.post_view, name='post'),
    path('feed/', views.feed_view, name='feed'),
    path('notifications/', views.notifications_view, name='notifications'),
]
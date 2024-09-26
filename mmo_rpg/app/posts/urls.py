from django.urls import path

from . import views
app_name = 'posts'

urlpatterns = [
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('post/<int:pk>', views.post_view, name='post'),
    path('feed/', views.feed_view, name='feed'),
    path('create-post/', views.create_post_view, name='create'),
    path('post-delete/<int:pk>', views.delete_post_view, name='delete'),
    path('search/', views.search_user_view, name='search'),
]
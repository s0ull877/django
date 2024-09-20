from django.urls import path

from . import views
app_name = 'posts'

urlpatterns = [
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('feed/', views.feed_view, name='feed')
]
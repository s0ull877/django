from django.urls import path

from users.views import register_user_view
app_name = 'users'

urlpatterns = [
    path('register/', register_user_view, name='register'),
]
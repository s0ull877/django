from django.urls import path

from users import views
app_name = 'posts'

urlpatterns = [
    path('profile/<str:username>', views.register_user_view, name='profile')
]
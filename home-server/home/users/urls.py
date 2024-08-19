from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required


from users.views import UserLoginView, UserProfileView, UserRegistrationView, cart_page, email_verification_view

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
    path('registration/', UserRegistrationView.as_view(), name='register'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
    path('cart/', login_required(cart_page), name='user_cart'),
    path('verification/<str:email>/<uuid:code>/', email_verification_view, name='verify'),
]

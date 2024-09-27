from django.urls import path

from users import views
app_name = 'users'

urlpatterns = [
    path('register/', views.register_user_view, name='register'),
    path('login/', views.login_user_view, name='login'),
    path('email-verification/<str:email>/<uuid:code>', views.logout_view, name='verify'),
    path('profile/edit/', views.profile_edit_view, name='edit-profile'),
    path('logout/', views.logout_view, name='logout'),

    path('about/', views.about_view, name='about'),
    path('axe-api/', views.axe_api_view, name='axe-api'),
    path('rules/', views.rules_view, name='rules'),
]
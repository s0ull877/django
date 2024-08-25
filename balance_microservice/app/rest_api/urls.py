from django.urls import path, include

from . import views

urlpatterns = [
    path('ballance-get/', views.GetUserBallance.as_view()),
    path('ballance-edit/', views.EditUserBallance.as_view())
]

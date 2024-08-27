from django.urls import path, include

from . import views

urlpatterns = [
    path('ballance-get/', views.GetUserBallance.as_view()),
    path('ballance-edit/', views.EditUserBallance.as_view()),
    path('ballance-send/', views.SendMoneyAPIView.as_view()),
    path('transactions/', views.GetUserTransaction.as_view())
]

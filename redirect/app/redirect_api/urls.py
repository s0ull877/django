from django.urls import path
from .views import RedirectCreateView, GetAuthToken

urlpatterns = [
    path('redirect-create/', RedirectCreateView.as_view()),
    path('get-token/', GetAuthToken().as_view()),
]
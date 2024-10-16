from django.urls import path
from .views import RedirectCreateView

urlpatterns = [
    path('redirect-create/', RedirectCreateView.as_view()),
]
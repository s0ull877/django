from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register('workers', views.WorkerViewSet)

urlpatterns = [
    path('link-create/', views.LinkCreateView.as_view()),
    path('sub-create/', views.SubCreateView.as_view()),
    path('', include(router.urls))
]

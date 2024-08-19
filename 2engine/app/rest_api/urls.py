from django.urls import path
from rest_framework import routers
from .views import TasksListViewSet, TaskViewSet

app_name = 'rest_api'

router = routers.SimpleRouter()
router.register(r'task', TaskViewSet)

urlpatterns = [
    path('list-tasks/', TasksListViewSet.as_view({'get':'list'})),
]

urlpatterns += router.urls
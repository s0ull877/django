from django.urls import path

from .views import TasksListView

app_name = 'tasks'

urlpatterns = [
    path('list/', TasksListView.as_view(), name='list')
]
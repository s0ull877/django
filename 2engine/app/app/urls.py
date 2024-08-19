from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_api.urls', namespace='api')),
    path('tasks/', include('tasks.urls', namespace='tasks')),
]

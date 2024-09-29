from django.urls import path
from .views import submitData


urlpatterns=[
    path('submitData/', submitData),
]
from django.urls import path

from main.views import AboutTemplateView, HomeTemplateView

app_name = 'main'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='index'),
    path('about/', AboutTemplateView.as_view(), name='about')
]

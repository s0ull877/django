from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from common.views import TitleMixin


# Create your views here.
def index(request):
    return HttpResponseRedirect(reverse('main:index'))

class HomeTemplateView(TitleMixin, TemplateView):

    template_name = 'main/index.html'
    title = 'Home - главная'


class AboutTemplateView(TitleMixin, TemplateView):

    template_name = 'main/about.html'
    title = 'Home - Информация'

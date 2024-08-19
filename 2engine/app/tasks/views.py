from django.views.generic.list import ListView

from .models import Task

from common.views import TitleMixin

from .utils import q_search


class TasksListView(TitleMixin, ListView):

    model = Task
    template_name = "tasks/index.html"
    title = 'Tasks List'
    paginate_by = 15

    def get_queryset(self):
        
        queryset = super().get_queryset()

        params = self.request.GET
        query = params.get('q')
        
        if query:
            queryset = q_search(query)

        return queryset
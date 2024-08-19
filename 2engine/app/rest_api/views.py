from rest_framework import viewsets, status, mixins, response
from rest_framework.response import Response

from tasks.serializers import TaskSerializer, Task

from tasks.tasks import process

class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request):
        
        return Response(data={'errors': 'This method now allowed! Use another endpoint.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def create(self, request, *args, **kwargs):

        data= request.data.dict()
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():

            task = serializer.save(**data)
            process.delay(task.id)

            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(data={"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class TasksListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
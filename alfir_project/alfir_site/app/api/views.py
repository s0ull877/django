from rest_framework import viewsets, views, status, response, mixins
from rest_framework.permissions import IsAdminUser
from workers.models import Worker, Link
from workers.serializers import WorkerReadSerializer, WorkerWriteSerializer, LinkWriteSerializer, SubWriteSerializer
from django.core import serializers

class LinkCreateView(views.APIView):

    permission_classes = [IsAdminUser]

    def post(self,request):

        data= request.data

        serializer = LinkWriteSerializer(data=data)

        if serializer.is_valid():

            link = serializer.save(**{'name': data['name'], 'telegram_link': data['telegram_link']})

            return response.Response(data={'id': link.id}, status=status.HTTP_201_CREATED, content_type='application/json')

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class WorkerViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin ,mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Worker.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):

        if self.action == 'create':
            return WorkerWriteSerializer

        return WorkerReadSerializer

    def create(self, request, *args, **kwargs):

        data= request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():

            worker = serializer.save(**{'worker_tg_id': data['worker_tg_id'], 'name': data['name'], 'phone': data['phone']})

            return response.Response(data={'id': worker.id}, status=status.HTTP_201_CREATED)

        return response.Response(data={"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class SubCreateView(views.APIView):

    permission_classes = [IsAdminUser]

    def post(self,request):

        data= request.data
        serializer = SubWriteSerializer(data=data)

        if serializer.is_valid():

            sub = serializer.save(**{'link_id': data['link_id'], 'worker_id': data['worker_id'],'created': data['created']})

            return response.Response(data={'id': sub.id}, status=status.HTTP_201_CREATED, content_type='application/json')

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

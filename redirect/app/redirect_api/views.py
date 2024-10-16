from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework import response, status

from redirect.serializers import RedirectSerializer

class RedirectCreateView(CreateModelMixin, APIView):

    # permission_classes = [IsAdminUser]

    def post(self,request):

        serializer = RedirectSerializer(data=request.data)

        if serializer.is_valid():

            redirect_obj = serializer.save(redirect_to=request.data.get('redirect_to'))

            return response.Response(data={'redirect_url': redirect_obj.get_redirect_uri()}, status=status.HTTP_201_CREATED, content_type='application/json')

        return response.Response(data={'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
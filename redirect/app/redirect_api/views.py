from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import response, status
from rest_framework.authtoken.models import Token


from redirect.serializers import RedirectSerializer

from django.contrib.auth import authenticate

class RedirectCreateView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self,request):

        serializer = RedirectSerializer(data=request.data)

        if serializer.is_valid():

            redirect_obj = serializer.save(redirect_to=request.data.get('redirect_to'))

            return response.Response(data={'redirect_url': redirect_obj.get_redirect_uri()}, status=status.HTTP_201_CREATED, content_type='application/json')

        return response.Response(data={'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class GetAuthToken(APIView):

    def post(self, request):

        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )

        if user is None:

            return response.Response(data={'errors':'Incorrect data!'}, status=status.HTTP_400_BAD_REQUEST)
        
        token, _ = Token.objects.get_or_create(user=user)

        return response.Response(data={'token': token.key}, status=status.HTTP_200_OK, content_type='application/json')



    

    
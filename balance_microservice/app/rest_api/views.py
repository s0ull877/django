from typing import Callable
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, generics, response, exceptions

from ballance.serializers import UserBallance, BallanceTransaction, UserBallanceSerializer, BallanceTransactionSerializer


def valid_post_data(request, required: dict[str, Callable]):

    arg_count=len(required)
    keys = list(required.keys())

    for key, key_type in required.items():

        try:
            data = request.data[key]
            request.data[key]= key_type(data)

        except KeyError:
            raise exceptions.ValidationError(detail={'detail': 'Method get {} required argument: {}!'.format(arg_count, ', '.join(keys))},
                                    code=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            raise exceptions.ValidationError(detail={'detail': f'"{key}" must be a {key_type}!'},
                        code=status.HTTP_400_BAD_REQUEST)
        
    return request

# получение баланса
# body - { 'user_id': int }
class GetUserBallance(generics.GenericAPIView):

    queryset=UserBallance.objects.all()
    serializer_class=UserBallanceSerializer
    required_post_fields={'user_id': int}


    def post(self, request):
            
        valid_post_data(request, self.required_post_fields)
        instance = get_object_or_404(self.get_queryset(), user_id=request.data['user_id'])
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)




# списание/пополнение
# body - { 'user_id': int, quantity: demical }
class EditUserBallance(mixins.UpdateModelMixin, generics.GenericAPIView):

    queryset=UserBallance.objects.all()
    serializer_class=UserBallanceSerializer
    required_post_fields={'quantity': float, 'user_id': int}

    def update(self, request):

        try:
            instance = get_object_or_404(self.get_queryset(), user_id=request.data['user_id'])
        except Http404:
            instance = self.get_queryset().model.objects.create(user_id=request.data['user_id'])

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return response.Response(serializer.data)    


    def post(self, request):


        valid_post_data(request, self.required_post_fields)
        
        return self.update(request)
    

# Перевод между счетатми
# body - { 'user_id': int, quantity: demical, 'recipient': int}
class SendMoneyAPIView(mixins.UpdateModelMixin, generics.GenericAPIView):

    queryset=UserBallance.objects.all()
    serializer_class=UserBallanceSerializer
    required_post_fields={'quantity': float, 'user_id': int, 'recipient': int}

    def update(self, request):

        instance = get_object_or_404(self.get_queryset(), user_id=request.data['user_id'])
        # казаось бы при первом зачислении должен создаваться счет, но я решил не делать этого,
        # чтобы избежать случайные переводы.
        recipient = get_object_or_404(self.get_queryset(), user_id=request.data['recipient'])



        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return response.Response(serializer.data)    

    def post(self, request):

        valid_post_data(request, self.required_post_fields)
        
        return self.update(request)
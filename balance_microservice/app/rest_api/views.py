from typing import Callable

from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status, mixins, generics, response, exceptions

from ballance.serializers import UserBallance, UserBallanceSerializer 

from .utils import transform_quantity

class CustomGenericView(generics.GenericAPIView):

    required_post_fields={'user_id': int}

    # для кастомных валидаций
    def custom_validation(self) -> None:
        pass

    # валидируем тело запроса, ключи и типы данных значений
    def valid_post_data(self) -> None:

        arg_count=len(self.required_post_fields)
        keys = list(self.required_post_fields.keys())

        for key, key_type in self.required_post_fields.items():

            try:
                data = self.request.data[key]
                self.request.data[key]= key_type(data)

            except KeyError:
                raise exceptions.ValidationError(detail={'detail': 'Method get {} required argument: {}!'.format(arg_count, ', '.join(keys))},
                                        code=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                raise exceptions.ValidationError(detail={'detail': f'"{key}" must be a {key_type}!'},
                            code=status.HTTP_400_BAD_REQUEST)
            
        self.custom_validation()
            

# получение баланса
# body - { 'user_id': int }
class GetUserBallance(CustomGenericView):

    queryset=UserBallance.objects.all()
    serializer_class=UserBallanceSerializer

    def post(self, request):
            
        self.valid_post_data()
        instance = get_object_or_404(self.get_queryset(), user_id=request.data['user_id'])
        serializer = self.get_serializer(instance)

        if request.query_params.get('currency') is not None:
            serializer.data['quantity'] = transform_quantity(quantity=instance.ballance, currency=request.query_params['currency'])
        
        return response.Response(serializer.data)


# списание/пополнение
# body - { 'user_id': int, quantity: demical }
class EditUserBallance(mixins.UpdateModelMixin, CustomGenericView):

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

        self.valid_post_data()
        
        return self.update(request)
    

# Перевод между счетатми
# body - { 'user_id': int, quantity: demical, 'recipient': int}
class SendMoneyAPIView(mixins.UpdateModelMixin, CustomGenericView):

    queryset=UserBallance.objects.all()
    serializer_class=UserBallanceSerializer
    required_post_fields={'quantity': float, 'user_id': int, 'recipient': int}


    def custom_validation(self):

        if self.request.data['quantity'] <= 0:
            raise exceptions.ValidationError(detail={'detail': 'quantity must be positive number'}, code=status.HTTP_400_BAD_REQUEST)
        
        if self.request.data['user_id'] == self.request.data['recipient']:
            raise exceptions.ValidationError(detail={'detail': 'sender and recipient with one user_id'}, code=status.HTTP_400_BAD_REQUEST)


    def update(self, request):
        # казаось бы при первом зачислении должен создаваться счет, но я решил не делать этого,
        # чтобы избежать случайные переводы.
        try:
            sender = get_object_or_404(self.get_queryset(), user_id=request.data['user_id'])
            recipient = get_object_or_404(self.get_queryset(), user_id=request.data['recipient'])
        except Http404:

            if 'sender' in locals():
                raise Http404('No ballance with user_id: {}'.format(request.data['recipient']))
            
            raise Http404('No recipient with user_id: {}'.format(request.data['user_id']))


        sender_serializer = self.get_serializer(sender, data={'quantity': request.data['quantity'] * -1}, partial=True)
        sender_serializer.is_valid(raise_exception=True)
        sender_serializer.save()

        recipient_serializer = self.get_serializer(recipient, data={'quantity': request.data['quantity']}, partial=True)
        recipient_serializer.is_valid(raise_exception=True)
        recipient_serializer.save()


        return response.Response(sender_serializer.data)   


    def post(self, request):

        self.valid_post_data()

        return self.update(request)
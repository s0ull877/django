import decimal
from time import timezone
from rest_framework import serializers, status, exceptions

from .models import UserBallance, BallanceTransaction

class UserBallanceSerializer(serializers.ModelSerializer):

    class Meta:

        model=UserBallance
        fields=('user_id','ballance',)

    def is_valid(self, *, raise_exception=True):
        
        self.initial_data['quantity']=decimal.Decimal(self.initial_data.get('quantity'))

        if self.instance.ballance + self.initial_data.get('quantity') < 0:
            raise exceptions.ValidationError(detail={'detail':'ballance cant will be less than zero.'}, code=status.HTTP_400_BAD_REQUEST)
        
        return super().is_valid(raise_exception=raise_exception)


    def save(self, **kwargs):

        # создание транзакции
        self.instance.ballance += self.initial_data.get('quantity')

        return super().save(**kwargs)


class BallanceTransactionSerializer(serializers.ModelSerializer):

    user_ballance=serializers.PrimaryKeyRelatedField(queryset=UserBallance.objects.all())

    class Meta:
        
        model=BallanceTransaction
        fields = ('user_ballance', 'quantity', 'service', 'description',)
        read_only_fields=('created_at',)


    def create(self, validated_data):
        
        validated_data['created_at'] = timezone.now()
        return super().create(validated_data)
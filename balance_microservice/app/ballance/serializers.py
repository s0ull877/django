from time import timezone
from rest_framework import serializers

from .models import UserBallance, BallanceTransaction

class UserBallanceSerializer(serializers.Serializer):

    class Meta:

        model=UserBallance
        fields=('user_id', 'ballance')


class BallanceTransactionSerializer(serializers.Serializer):

    user_ballance=serializers.PrimaryKeyRelatedField(queryset=UserBallance.object.all())

    class Meta:
        
        model=BallanceTransaction
        fields = ('user_ballance', 'quantity', 'service', 'description')
        read_only_fields=('created_at',)


    def create(self, validated_data):
        
        validated_data['created_at'] = timezone.now()
        return super().create(validated_data)
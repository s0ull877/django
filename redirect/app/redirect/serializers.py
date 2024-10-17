import string
from django.db.utils import IntegrityError
from django.utils.crypto import get_random_string
from django.conf import settings

from rest_framework import serializers

from .models import RedirectModel

settings.CHARACTERS = string.ascii_letters + string.digits

class RedirectSerializer(serializers.ModelSerializer):


    class Meta:
        model = RedirectModel
        fields = ('redirect_to','path',)


    def is_valid(self, raise_exception=False):

        if self.initial_data.get('path') is None:

            self.initial_data['path'] = get_random_string(length=10, allowed_chars=settings.CHARACTERS)
            
        return super().is_valid(raise_exception=raise_exception)
    

    def create(self, validated_data):

        ModelClass = self.Meta.model

        while True:

            try:
                instanse = ModelClass._default_manager.create(**validated_data)
            except IntegrityError:
                pass
            else:
                validated_data['path'] = get_random_string(length=10, allowed_chars=settings.CHARACTERS)
                break

        return instanse
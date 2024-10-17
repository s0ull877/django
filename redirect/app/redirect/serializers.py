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
        fields = ('redirect_to',)

    def create(self, validated_data):

        ModelClass = self.Meta.model

        # if generate_path() get non unique data, i try to generate new path
        while True:

            validated_data['path'] = get_random_string(length=10, allowed_chars=settings.CHARACTERS)

            try:
                instanse = ModelClass._default_manager.create(**validated_data)
            except IntegrityError:
                pass
            else:
                break

        return instanse
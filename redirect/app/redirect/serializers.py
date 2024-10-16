from django.db.utils import IntegrityError

from rest_framework import serializers
from .utils import generate_path

from .models import RedirectModel

class RedirectSerializer(serializers.ModelSerializer):


    class Meta:
        model = RedirectModel
        fields = ('redirect_to',)

    def create(self, validated_data):

        ModelClass = self.Meta.model

        # if generate_path() get non unique data, i try to generate new path
        while True:

            validated_data['path'] = generate_path()

            try:
                instanse = ModelClass._default_manager.create(**validated_data)
            except IntegrityError:
                pass
            else:
                break

        return instanse
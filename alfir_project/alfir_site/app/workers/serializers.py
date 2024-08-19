from rest_framework import serializers, fields

from .models import Link, Worker, Sub


class WorkerReadSerializer(serializers.ModelSerializer):

    class Meta:
        model=Worker
        fields = ('id', 'worker_tg_id', 'phone',)

class WorkerWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model=Worker
        fields = ('worker_tg_id', 'name', 'phone',)


class LinkWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model=Link
        fields = ('name', 'telegram_link',)


class SubWriteSerializer(serializers.ModelSerializer):

    link_id = serializers.PrimaryKeyRelatedField(
        queryset=Link.objects.all(), 
        source='link', write_only=True
        )
    worker_id = serializers.PrimaryKeyRelatedField(
        queryset=Worker.objects.all(), 
        source='worker', write_only=True
        )
    
    class Meta:

        model=Sub
        fields = ('link_id', 'worker_id', 'created',)

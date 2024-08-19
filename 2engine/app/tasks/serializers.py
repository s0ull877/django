from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    class Meta:

        model = Task
        fields = ['id', 'name', 'description', 'status']
        read_only_fields =('id','status',)

    def get_status(self, obj):
        return dict(Task.STATUSES).get(obj.status)
    
    # def is_valid(self, *, raise_exception=False):
    #     data = self.initial_data
    #     return super().is_valid(raise_exception=raise_exception)
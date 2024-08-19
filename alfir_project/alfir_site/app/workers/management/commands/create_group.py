from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from ._utils import info
from django.contrib.auth import get_user_model
import os

Users = get_user_model()
MODELS = ['Подписчик', 'Link', 'Аккаунт']
username = os.getenv('STAFF_USERNAME', default='staffuser3')


class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'
    name = 'GROUP'
    model_class = Group

    @info
    def handle(self, *args, **options):
        new_group, created = Group.objects.get_or_create(name='CustomGroup')
        for model in MODELS:
            name = 'Can {} {}'.format('view', model)
            print("Creating {}".format(name))

            try:
                model_add_perm = Permission.objects.get(name=name)
            except Permission.DoesNotExist:
                self.stdout.write("Permission not found with name '{}'.".format(name))
                continue

            new_group.permissions.add(model_add_perm)

        new_group.user_set.add(Users.objects.get(username=username))
        print("Created default group and permissions.")
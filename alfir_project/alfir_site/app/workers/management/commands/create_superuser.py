import os
from typing import Any
from ._utils import info
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

username= os.getenv('ADMIN_USERNAME', default='root')
email= os.getenv('ADMIN_EMAIL', default='root@mail.com')
password = password=os.getenv('ADMIN_PASSWORD', default='root')

class Command(BaseCommand):

    model_class = User
    name = 'SuperUser'

    @info
    def handle(self, *args: Any, **options: Any) -> str | None:
        self.model_class.objects.create_superuser(
            username=username, email=email, password=password
        )
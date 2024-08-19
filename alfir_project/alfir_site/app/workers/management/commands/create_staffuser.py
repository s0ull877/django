import os
from typing import Any
from ._utils import info
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

username= os.getenv('STAFF_USERNAME', default='staffuser3')
email= os.getenv('STAFF_EMAIL', default='staffuser@mail.com')
password = password=os.getenv('STAFF_PASSWORD', default='staffuser3')

class Command(BaseCommand):

    model_class = User
    name = 'StaffUser'

    @info
    def handle(self, *args: Any, **options: Any) -> str | None:
        self.model_class.objects.create_user(
            username=username, email=email, password=password, is_staff=True
        )
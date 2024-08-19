import os
from typing import Any
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from users.utils import info

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME',default='root')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', default='root@mail.com')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', default='root')

User = get_user_model()

class Command(BaseCommand):
    
    _class=User
    name='SUPERUSER'

    @info
    def handle(self, *args: Any, **options: Any) -> str | None:
        self._class.objects.create_superuser(
                ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD
        )
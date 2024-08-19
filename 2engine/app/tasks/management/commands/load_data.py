import random
from string import ascii_letters, digits

from tasks.models import Task
from django.core.management import BaseCommand
from django.db import IntegrityError

from .utils import info

WORDS = ['section', 'rabbit', 'tiger', 'can', 'love', 'you', 'fast', 'wait', 'flower']


class Command(BaseCommand):
    
    model_class = Task
    name = 'Tasks'

    @staticmethod
    def random_desc():

        words = random.choices(WORDS, k=random.randint(1, 6))
        return ' '.join(words)

    @info
    def handle(self, *args, **kwargs):
        for i in range(1,40):

            task = Task.objects.create(
                name=f'task{i}',
                description=self.random_desc(),
                status=2
            )
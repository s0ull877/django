from typing import Iterable
from django.db import models

class Task(models.Model):

    QUEUE = 0
    IN_PROGRESS = 1
    COMPETED = 2

    STATUSES = (
        (QUEUE, 'Queue.'),
        (IN_PROGRESS, 'In progress...'),
        (COMPETED, 'Completed!'),
    )

    name = models.CharField(max_length=150, verbose_name='Task name')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    status = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Status', default=QUEUE, choices=STATUSES)

    class Meta:

        verbose_name_plural = 'Tasks'


    def __str__(self) -> str:
        return self.name

    

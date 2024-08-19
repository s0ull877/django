from celery import shared_task
from .models import Task
from time import sleep

@shared_task()
def process(task_id: int):

    task = Task.objects.get(id=task_id)
    task.status = Task.IN_PROGRESS 
    task.save()

    sleep(10)

    task.status = Task.COMPETED
    task.save()

from celery import shared_task


from notifications.models import EmailNotification
from users.models import User


@shared_task
def send_email(user_id, text):

    user = User.objects.get(pk=user_id)

    EmailNotification.objects.create(
        to=user,
        message=text,
        manual=False
    )
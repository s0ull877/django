import datetime
from celery import shared_task
from django.utils.timezone import now


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


# celery -A app beat -l INFO
@shared_task
def clear_nonmanual_mails():

    # удаляем авоматически отправленные сообщения, которым больше недели
    expired_time = now() - datetime.timedelta(days=7)
    try:
        EmailNotification.objects.filter(created_at__lte=expired_time, manual=False).delete()
    except Exception as ex:
        print(ex)

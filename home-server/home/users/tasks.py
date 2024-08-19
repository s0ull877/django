import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import User, EmailVerification

@shared_task
def send_email_task(user: User):
    
    expiration = now() + timedelta(minutes=15)
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()
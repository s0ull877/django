from django.contrib import admin
from .models import Notification, EmailNotification

admin.site.register(Notification)
admin.site.register(EmailNotification)

from django.contrib import admin
from .models import UserBallance, BallanceTransaction

admin.site.register(UserBallance)
admin.site.register(BallanceTransaction)


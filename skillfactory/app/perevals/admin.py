from django.contrib import admin

# Register your models here.
from .models import Pereval,PerevalImage,PerevalLevel,Coordinates   

admin.site.register(Pereval)
admin.site.register(PerevalLevel)
admin.site.register(PerevalImage)
admin.site.register(Coordinates)

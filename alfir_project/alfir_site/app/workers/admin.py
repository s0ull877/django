from datetime import timedelta, datetime
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Worker, Link, Sub


class CreatedListFilter(admin.SimpleListFilter):

    title = _("Дата создания")

    parameter_name = "created"

    def lookups(self, request, model_admin):
        

        return [
            ("today", _("Сегодня")),
            ("this_week", _("Неделя")),
            ("this_mounth", _("Месяц")),
        ]

    def queryset(self, request, queryset):

        value = self.value()  
        if not value:
            return queryset
        
        
        if value == 'today':

            return queryset.filter(created__date=datetime.now())
        
        if value == 'this_week':

            end_date = datetime.now()
            start_date = end_date - timedelta(weeks=1)
            return queryset.filter(created__range=(start_date, end_date))
        
        if value == 'this_mounth':

            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            return queryset.filter(created__range=(start_date, end_date))


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):

        list_display=(
            'name',
            'created',
        )
        fields = (
            'id', 
            'name',
            'telegram_link',
            'created',
        )
        readonly_fields = ('id', 'created','telegram_link',)

        list_filter = (CreatedListFilter,)
        search_fields = ('name','telegram_link')
        ordering = ('-id',)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
     
        list_display=(
            'name',
            'created',
        )
        fields = (
            'id', 
            'name',
            'phone',
            'worker_tg_id',
            'created',
        )
        readonly_fields = ('id', 'created','phone', 'worker_tg_id',)
        list_filter = (CreatedListFilter,)
        search_fields = ('name', 'worker_tg_id',)
        ordering = ('-id',)



@admin.register(Sub)
class SubAdmin(admin.ModelAdmin):
        
        list_display=(
            'worker',
            'link',
            'created',
        )
        list_filter = (CreatedListFilter,'link__name')
        readonly = ('__all__',)
        search_fields = ('worker__name', 'link__name',)
        ordering = ('-id',)
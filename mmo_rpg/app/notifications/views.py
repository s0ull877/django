from django.shortcuts import render
from django.http.response import JsonResponse

from .models import Notification

def notifications_view(request):

    notifications = Notification.objects.select_related('owner', 'to_post').filter(status=None, to_post__owner=request.user).order_by('-date')
    context={
        'title': 'Оповещения',
        'notifications': notifications
    }

    return render(request=request, template_name='notifications/notifications.html', context=context)


def change_view(request):

    notification = Notification.objects.get(pk=request.POST.get('notification_id'))
    notification.status = True if request.POST.get('value') == 'true' else False
    notification.save()

    return JsonResponse({'status_code': 200})

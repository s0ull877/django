from django.shortcuts import render
from django.http.response import JsonResponse

from .models import Notification
from posts.models import Post

from django.contrib.auth.decorators import login_required

@login_required()
def notifications_view(request):

    notifications = Notification.objects.select_related('owner', 'to_post').filter(status=None, to_post__owner=request.user).order_by('-date')
    context={
        'title': 'Оповещения',
        'notifications': notifications
    }

    return render(request=request, template_name='notifications/notifications.html', context=context)

@login_required()
def change_view(request):

    notification = Notification.objects.get(pk=request.POST.get('notification_id'))
    notification.status = True if request.POST.get('value') == 'true' else False
    notification.save()

    return JsonResponse({'status_code': 200})

@login_required()
def like_view(request, pk):

    post = Post.objects.get(pk=pk)

    value = True if request.POST.get('value') == 'true' else False

    if value:
        post.liked_users.add(request.user)
    else:
        post.liked_users.remove(request.user)

    return JsonResponse({'status_code': 200})
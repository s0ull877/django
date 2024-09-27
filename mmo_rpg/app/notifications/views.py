from django.db.models import F
from django.http import Http404
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


def change_view(request):

    try:

        notification = Notification.objects.select_related('to_post').get(pk=request.POST['notification_id'])

        if notification.to_post.owner == request.user:

            notification.status = True if request.POST['value'] == 'true' else False
            notification.save()

            return JsonResponse({'success': True,}, status=200)
        
        raise Http404('You cant approve/eject this comment')

    except KeyError as ex:
        return JsonResponse({'success': False, 'error': 'Required body argument: {}'.format(ex.__str__())}, status=400)    

    except Http404 as ex:
        return JsonResponse({'success': False, 'error': ex.__str__()}, status=400)       

    except Exception as ex:
        return JsonResponse({'success': False, 'error': ex.__str__()}, status=500)


def like_view(request, pk):

    try:
        
        if request.user.is_authenticated:

            post = Post.objects.get(pk=pk)
            value = True if request.POST['value'] == 'true' else False

            if value:
                post.liked_users.add(request.user)
            else:
                post.liked_users.remove(request.user)

            return JsonResponse({'success': True,}, status=200)
        
        raise Http404('You cant like this posts')

    except KeyError as ex:
        return JsonResponse({'success': False, 'error': 'Required body argument: {}'.format(ex.__str__())}, status=400)    

    except Http404 as ex:
        return JsonResponse({'success': False, 'error': ex.__str__()}, status=400)       

    except Exception as ex:
        return JsonResponse({'success': False, 'error': ex.__str__()}, status=500)
    

def delete_view(request):

    try:
        
        data = request.POST.dict()
    
        notf = Notification.objects.get(pk=int(data['notification_id']))

        if request.user.username in (data['post_owner'], data['notf_owner']):

            notf.delete()

            return JsonResponse({'status_code': 204, 'pk': data['notification_id']})
        
        raise Http404('You cant delete this comment.')

    except KeyError as ex:
        return JsonResponse({'success': False, 'error': 'Required body argument: {}'.format(ex.__str__())}, status=400)  
    
    except Http404 as ex:
        return JsonResponse({'success': False, 'error': ex.__str__()}, status=400)       

    except Exception as ex:
        return JsonResponse({'success': False, 'error': ex.__str__()}, status=500)
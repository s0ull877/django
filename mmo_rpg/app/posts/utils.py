import os
import re
from uuid import uuid4
from django.conf import settings

from django.db.models import Count, QuerySet, Q
from django.db.models.manager import Manager


def custom_upload(instance, filename):

    post=instance.to_post
    user=post.owner
    filename = uuid4()

    try:
    
        dir_path = settings.MEDIA_ROOT / 'posts_images' / user.id
        os.mkdir(dir_path)
    
    except Exception as e:
        pass

    finally:
    
        post=instance.to_post
        user=post.owner
        filename = uuid4()
    
        return f'posts_images/{user.id}/{filename}.jpg' 
    


# comments_count считает даже неактивные коменты
def full_posts_query(manager: Manager, get_by:dict=None, **filters) -> QuerySet:

    if get_by:

        post=manager.select_related('category', 'owner'). \
            prefetch_related('postimage_set').prefetch_related('liked_users'). \
            annotate(comments_count=Count('notification__id', filter=Q(notification__status=True), distinct=True)). \
            annotate(likes=Count('liked_users__id', distinct=True)).get(**get_by)
        
        return post

    if not filters:

        posts=manager.select_related('category', 'owner'). \
            prefetch_related('postimage_set').prefetch_related('liked_users'). \
            annotate(comments_count=Count('notification__id',filter=Q(notification__status=True), distinct=True)). \
            annotate(likes=Count('liked_users__id', distinct=True))
        
    else:

        posts=manager.select_related('category', 'owner'). \
            prefetch_related('postimage_set').prefetch_related('liked_users'). \
            annotate(comments_count=Count('notification__id',filter=Q(notification__status=True), distinct=True)). \
            annotate(likes=Count('liked_users__id', distinct=True)).filter(**filters)       
    
    return posts

def get_redirect_url(request) -> str:

    uri=request.GET['to']
    
    if bool(re.match(r'^/post/\d+$', uri)):

        return settings.HOSTNAME + f'/profile/{request.user.username}'

    for k,v in request.GET.dict().items():
        
        if k == 'to':
            continue

        uri += f'&{k}={v}'

    return settings.HOSTNAME + uri
import os
from uuid import uuid4
from django.conf import settings

from django.db.models import Count, QuerySet
from django.db.models.manager import Manager


def custom_upload(instance, filename):

    post=instance.to_post
    user=post.owner
    filename = uuid4()

    try:
    
        dir_path = settings.MEDIA_ROOT / 'posts_images' / user.username
        os.mkdir(dir_path)
    
    except Exception as e:
        pass

    finally:
    
        post=instance.to_post
        user=post.owner
        filename = uuid4()
    
        return f'posts_images/{user.username}/{filename}.jpg' 
    


def full_posts_query(manager: Manager, get_by:dict=None, **filters) -> QuerySet:

    if get_by:

        post=manager.select_related('category', 'owner'). \
            prefetch_related('postimage_set'). \
            annotate(likes_count=Count('liked_users__id')).annotate(comments_count=Count('notification__id')).get(**get_by)
        
        return post

    if not filters:

        posts=manager.select_related('category', 'owner'). \
            prefetch_related('postimage_set'). \
            annotate(likes_count=Count('liked_users__id')).annotate(comments_count=Count('notification__id'))
        
    else:

        posts=manager.select_related('category', 'owner'). \
            prefetch_related('postimage_set'). \
            annotate(likes_count=Count('liked_users__id')).annotate(comments_count=Count('notification__id')).filter(**filters)       
    
    return posts
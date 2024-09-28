import os
import re
from uuid import uuid4

from django.conf import settings
from django.db.models import Count, QuerySet, Q
from django.db.models.manager import Manager
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from users.models import User

def custom_upload(instance, filename):

    post=instance.to_post
    user=post.owner
    filename = uuid4()

    try:
    
        # стараюсь фотки постов юзера привязывать к дирректории с его id
        dir_path = settings.MEDIA_ROOT / 'posts_images' / user.id
        os.mkdir(dir_path)
    
    except Exception as e:
        pass

    finally:
    
        user=instance.to_post.user
        filename = uuid4()
    
        return f'posts_images/{user.id}/{filename}.jpg' 
    


def full_posts_query(manager: Manager, get_by:dict=None, **filters) -> QuerySet:
# сокращаю количество запросов к базе данных через select_related, prefetch и пр.

    # если нужен 1 эелемент, например для страницы с одним постом
    if get_by:

        post=manager.select_related('category', 'owner'). \
            prefetch_related('postimage_set').prefetch_related('liked_users'). \
            annotate(comments_count=Count('notification__id', filter=Q(notification__status=True), distinct=True)). \
            annotate(likes=Count('liked_users__id', distinct=True)).get(**get_by)          #distint - без повторов
        
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


def q_search(query:str):

    vector = SearchVector("username")
    query = SearchQuery(query)
    
    users = User.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by('-rank')

    return users
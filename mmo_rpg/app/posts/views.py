from django.shortcuts import render
from django.db.models import Count

from posts.models import Post
from users.models import User


def profile_view(request, username):


    user = User.objects.get(username=username) 

    posts= user.post_set.select_related('category', 'owner'). \
        prefetch_related('postimage_set'). \
        annotate(likes_count=Count('liked_users__id')).annotate(comments_count=Count('notification__id'))
    
    context={
        'title': f'Профиль пользователя {user.username}',
        'owner': user,
        'posts' : posts
    }

    return render(request=request, template_name='posts/profile.html', context=context)


def feed_view(request, *args):

    data = request.GET.dict()

    if data.get('role'):

        posts = Post.objects.select_related('category', 'owner'). \
            prefetch_related('postimage_set'). \
            annotate(likes_count=Count('liked_users__id')).annotate(comments_count=Count('notification__id')).filter(category__slug=data['role'])
    
    else:

        posts = Post.objects.select_related('category', 'owner'). \
            prefetch_related('postimage_set'). \
            annotate(likes_count=Count('liked_users__id')).annotate(comments_count=Count('notification__id'))


    if data.get('filter') == 'popular':
        posts = posts.order_by('-likes_count')


    context={
        'title': 'Новости - Аксевич',
        'posts': posts
    }

    return render(request=request, template_name='posts/feed.html', context=context)
from django.shortcuts import render

from posts.models import Post
from users.models import User

from .utils import full_posts_query


def profile_view(request, username):


    user = User.objects.get(username=username) 

    posts = full_posts_query(user.post_set)
    
    context={
        'title': f'Профиль пользователя {user.username}',
        'owner': user,
        'posts' : posts
    }

    return render(request=request, template_name='posts/profile.html', context=context)


def feed_view(request, *args):

    data = request.GET.dict()

    if data.get('role'):

        posts = full_posts_query(Post.objects, category__slug=data['role'])
    
    else:

        posts = full_posts_query(Post.objects)

    if data.get('filter') == 'popular':
        posts = posts.order_by('-likes_count')
    else:
        posts = posts.order_by('-created_at')



    context={
        'title': 'Новости - Аксевич',
        'posts': posts
    }

    return render(request=request, template_name='posts/feed.html', context=context)
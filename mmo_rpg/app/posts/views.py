from django.db.models import Count
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render

from posts.models import Post, PostImage
from notifications.models import Notification
from posts.templatetags.categories_tag import categories_tag
from users.models import User

from .utils import full_posts_query, get_redirect_url, q_search
from .forms import CommentForm, CreatePostForm

from django.contrib.auth.decorators import login_required

def profile_view(request, username):


    user = User.objects.get(username=username)  if request.user.username != username else request.user

    posts = full_posts_query(user.post_set).order_by('-created_at')
    
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
        posts = posts.order_by('-likes')
    else:
        posts = posts.order_by('-created_at')


    context={
        'title': 'Новости - Аксевич',
        'posts': posts
    }

    return render(request=request, template_name='posts/feed.html', context=context)


def post_view(request, pk):

    post = full_posts_query(Post.objects, get_by={'pk': pk})
    message = None

    if request.method == 'POST':

        form=CommentForm(request.POST)

        if form.is_valid():

            Notification.objects.create(owner=request.user, to_post=post, text=form.cleaned_data['comment'])
            message = f'Комментарий отправлен!'
            if request.user != post.owner:
                message += f'Дождитесь когда {post.owner.username} примет решение.' 

        else:

            message =form.errors

    notifications = Notification.objects.select_related('owner').filter(status=True, to_post=post.id).order_by('-date')
    
    context = {
        'title': f'Публикация {post.owner.username}',
        'post': post,
        'notifications': notifications,
        'form': CommentForm(),
        'message': message
    }

    return render(request=request, template_name='posts/post.html', context=context)

@login_required()
def create_post_view(request):

    context = {
        'title': 'Новая запись',
        'message': ''
    }

    if request.method == 'POST':

        category = categories_tag().filter(id=int(request.POST.get('category'))).first()
        form=CreatePostForm(request.POST, request.FILES)

        if form.is_valid() and category:

            post = Post.objects.create(
                owner=request.user,
                text=form.cleaned_data['text'],
                category=category
            )

            # ! Я ПОКА ХЗ КАК ИНАЧЕ(
            for file in ['image1', 'image2', 'image3']:

                image = form.cleaned_data[file]
                if image is not None:
                    PostImage.objects.create(to_post=post, image=image)


            return redirect(to='posts:profile', username=request.user.username)

        else:

            context['message'] = f'Ошибка: {form.errors}'

    else:

        context['form']=CreatePostForm()


    return render(request=request, template_name='posts/create-post.html', context=context)


def delete_post_view(request, pk):

    redirect_to= get_redirect_url(request=request)

    post: Post = Post.objects.select_related('owner').get(pk=pk)
    if request.user == post.owner:

        ...
        post.delete()


    return redirect(to=redirect_to) 


def search_user_view(request):
        

    if request.method == 'POST':

        query = request.POST['q']

        users = q_search(query=query)

        context={
            'query': query,
            'title': f'Пользователи \'{query}\'',
            'users': users
        }

        return render(request=request, template_name='posts/users_list.html', context=context)

    elif request.user.is_authenticated:

        context={
            'title': f'Пользователь',
            'users': [request.user]
        }

        return render(request=request, template_name='posts/users_list.html', context=context)

    else:

        return Http404()
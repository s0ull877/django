from django.shortcuts import render

from users.models import User


def profile_view(request, username):

    user = User.objects.get(username=username)
    context={
        'title': f'Профиль пользователя {user.username}',
        'owner': user,
        'posts' : user.post_set.all()
    }

    return render(request=request, template_name='posts/profile.html', context=context)
    ...
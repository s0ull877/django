from django.conf import settings


def user_avatar_upload(instance, *args):
    # чтобы лишний раз не засорять дирректории, привязал автатар к id

    return settings.MEDIA_ROOT / 'users_images' /f'{instance.id}_avatar.jpg'
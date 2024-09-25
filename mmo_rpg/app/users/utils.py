from django.conf import settings

def user_avatar_upload(instance, *args):

    return settings.MEDIA_ROOT / 'users_images' /f'{instance.id}_avatar.jpg'
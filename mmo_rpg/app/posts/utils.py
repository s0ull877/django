from django.conf import settings

from uuid import uuid4
import os

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
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailOrUsernameModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None):

        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except user.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

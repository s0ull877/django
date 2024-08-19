from typing import Any

from django import forms

from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError

from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from users.models import User
from users.tasks import send_email_task




class UserLoginForm(AuthenticationForm):

    username = forms.CharField()
    password = forms.CharField()


    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
        "is_not_veryfied":_("This account is not verifyed. Check your email."),
    }


    def confirm_login_allowed(self, user):

        if not user.is_verified:
            raise ValidationError(
                self.error_messages["is_not_veryfied"],
                code="is_not_veryfied",
            )

        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )


    class Meta:

        model = User
        fields = ('username','password')


class UserProfileForm(UserChangeForm):

    image = forms.ImageField()

    first_name = forms.CharField()

    last_name = forms.CharField()

    username = forms.CharField(required=False)

    email = forms.EmailField(required=False)


    class Meta:

        model = User
        fields = ('image','first_name','last_name')



class UserRegistrationForm(UserCreationForm):

    first_name = forms.CharField()

    last_name = forms.CharField()

    username = forms.CharField()

    email = forms.EmailField()

    password1 = forms.CharField()

    password2 = forms.CharField()


    class Meta:

        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')



    def save(self, commit: bool = ...) -> Any:

        user = super().save(commit)

        send_email_task.delay(user)
    
        return user

from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import  User

class UserRegistrationForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "custom-placeholder",
        'placeholder': "username"
        }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': "custom-placeholder",
        'placeholder': "example@gmail.com"
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "custom-placeholder",
        'placeholder': "Пароль"
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "custom-placeholder",
        'placeholder': "Подтвердите пароль"
        }))


    class Meta:

        model = User
        fields = ('username', 'email', 'password1', 'password2')

    
    def save(self, commit=True):
        
        user = super(UserRegistrationForm, self).save(commit=True)

        # send_email_verification.delay(user.id)

        return user
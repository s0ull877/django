import re
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

    def clean(self):

        cleaned_data = super(UserRegistrationForm, self).clean()
        username = cleaned_data.get('username')
        
        if bool(re.search('[а-яА-Я]', username)):
            self.add_error('username', 'Russian words are not allowed in username.')
        
        return cleaned_data

    def save(self, commit=True):
        
        user = super(UserRegistrationForm, self).save(commit=True)

        # send_email_verification.delay(user.id)

        return user
    

class UserLoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "custom-placeholder",
        'placeholder': "Email или username"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "custom-placeholder",
        'placeholder': "Пароль"
    }))


class EditProfileForm(forms.Form):

    user=None

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':"custom-placeholder", 
        'name':"username",
        'placeholder':"Придумайте username",
        }), required=True)
    
    status = forms.CharField(widget=forms.Textarea(attrs={
        'class':"custom-placeholder", 
        'name':"status",
        'placeholder':"Ваш статус",
        'rows':"3"
    }), required=False)
    
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'name':'image', 
        'id':"new-profile-pic", 
        'class':"custom-placeholder"
        }), required=False)
    
    
    def clean_username(self):

        username = self.cleaned_data.get('username')

        user = User.objects.filter(username=username).first()

        if user is not None and user != self.user:
            
            self.add_error('username', 'This username is busy')

        elif bool(re.search('[а-яА-Я]', username)):
        
            self.add_error('username', 'Russian words are not allowed in username.')
        
        else:
            
            return username

    def save(self) -> User:

        if self.cleaned_data['image'] is None:

            self.cleaned_data['image'] = self.user.image

        self.user.username=self.cleaned_data['username']
        self.user.status=self.cleaned_data['status']
        self.user.image=self.cleaned_data['image']
        self.user.save()

        return self.user
    

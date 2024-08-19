from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


# миксины должны идти перед классом вью
class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    
    model = User
    form_class = UserRegistrationForm
    template_name=r'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Для окончания регистрации, перейдите по ссылке, отправленной вам на почту!'
    title = 'Store - Авторизация'



class UserProfileView(TitleMixin, UpdateView):

    model = User
    form_class = UserProfileForm
    template_name=r'users/profile.html'
    title = 'Store - Личный кабинет'


    def get_success_url(self):

        return reverse_lazy('users:profile', args=(self.object.id,))



class UserLoginView(TitleMixin, LoginView):
   
    template_name=r'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Регистрация'



class EmailVerificationView(TitleMixin,TemplateView):
    
    title = 'Store - Подтверждение электронной почты'
    template_name = r'users/email_verification.html'


    def get(self, request, *args, **kwargs):

        code = kwargs['code']
        user =User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)

        if email_verification.exists() and not email_verification.first().is_expired():

            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
            
        else:

            return HttpResponseRedirect(reverse('index'))

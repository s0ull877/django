from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

from carts.models import HomeCart
from users.models import User, EmailVerification
from carts.models import HomeCart



class UserLoginView(TitleMixin, LoginView):

    template_name = "users/login.html"
    form_class = UserLoginForm
    title = 'Home - Авторизация'

    def post(self, request, *args, **kwargs):

        form = self.get_form()
        if form.is_valid():
            self.session_key = request.session.session_key
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        

    def form_valid(self, form):
        
        user = form.get_user()
        auth_login(self.request, user)

        if self.session_key:
            HomeCart.objects.filter(session_key=self.session_key).update(user=user)
        
        return HttpResponseRedirect(self.get_success_url())



class UserProfileView(TitleMixin, UpdateView):

    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Home - Личный кабинет'

    def get_success_url(self):

        return reverse_lazy('users:profile', args=(self.object.id,))
    
    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        if request.user == self.object:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest(status=404)
        
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        if request.user == self.object:
            return super().post(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest(status=404)

    

class UserRegistrationView(SuccessMessageMixin, TitleMixin, CreateView):

    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    title = 'Home - Регистрация'
    success_url = reverse_lazy('users:login')
    success_message = 'Для окончания регистрации, перейдите по ссылке, отправленной вам на почту!'





def cart_page(request):

    context = {'title': 'Home - Корзина'}

    return HttpResponse(render(request, 'carts/user_basket.html', context))


def email_verification_view(request, email, code):
    
    if request.method == 'GET':

        user = User.objects.get(email=email)
        verification = EmailVerification.objects.get(code=code)
        if verification.is_expired() or not verification.active:

            messages.warning(request, 'Данная ссылка неактивна!')
            return redirect('main:index')
        
        else:

            session_key = request.session.session_key
            auth_login(request, user)

            verification.active = False
            verification.save()

            if session_key:
                HomeCart.objects.filter(session_key=session_key).update(user=user)

            messages.success(request, 'Ваша почта верифицирована!')
            return redirect('main:index')
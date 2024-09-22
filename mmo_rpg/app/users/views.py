from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import UserRegistrationForm, UserLoginForm



def register_user_view(request):

    if request.method == 'GET':

        context = {
            'form': UserRegistrationForm()
        }

    else: 
        
        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            form.save()
            context = {'title': 'Проверьте почту', 'email': form.data['email']}
            return render(request=request, template_name='send-email.html', context=context)

        context = {
            'form': form
        }

    return render(request=request, template_name='users/register.html', context=context)


def login_user_view(request):

    if request.method == 'GET':

        context = {
            'form': UserLoginForm()
        }

        return render(request=request, template_name='users/login.html', context=context)

    else: 

        form=UserLoginForm(request.POST)
        context = {
            'form': form
        }

        if form.is_valid():

            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is None:
                
                context['message'] = 'Введены неверные данные!'
                return render(request=request, template_name='users/login.html', context=context)

            elif not user.is_verified_email:

                context['message'] = 'Ваша почта не подтверждена!'
                return render(request=request, template_name='users/login.html', context=context)

            else:

                login(request=request, user=user)
                return redirect(to='posts:profile', username=user.username)
            
        else:

            return render(request=request, template_name='users/login.html', context=context)



# class UserProfileView(UpdateView):

#     model = User
#     form_class = UserProfileForm
#     template_name=r'users/edit-profile.html'


#     def get_success_url(self):

#         return reverse_lazy('users:edit-profile', args=(self.object.id,))



# class EmailVerificationView(TemplateView):
    
#     title = 'Store - Подтверждение электронной почты'
#     template_name = r'users/email_verification.html'


#     def get(self, request, *args, **kwargs):

#         code = kwargs['code']
#         user =User.objects.get(email=kwargs['email'])
#         email_verification = EmailVerification.objects.filter(user=user, code=code)

#         if email_verification.exists() and not email_verification.first().is_expired():

#             user.is_verified_email = True
#             user.save()
#             return super(EmailVerificationView, self).get(request, *args, **kwargs)
            
#         else:

#             return HttpResponseRedirect(reverse('index'))


def about_view(request):

    return render(request=request, template_name='about-us.html')

def axe_api_view(request):

    return render(request=request, template_name='axe-api.html')

def rules_view(request):

    return render(request=request, template_name='rules.html')
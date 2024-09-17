from django.shortcuts import render

from .forms import UserRegistrationForm

from django.views.generic.edit import CreateView, UpdateView

def register_user_view(request):



    if request.method == 'GET':

        context = {
            'form': UserRegistrationForm()
        }

    
    else: 
        
        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            form.save()

            return render(request=request, template_name='users/email_send.html')

        context = {
            'form': form
        }

    return render(request=request, template_name='users/register.html', context=context)




# class UserProfileView(UpdateView):

#     model = User
#     form_class = UserProfileForm
#     template_name=r'users/edit-profile.html'


#     def get_success_url(self):

#         return reverse_lazy('users:edit-profile', args=(self.object.id,))



# class UserLoginView( LoginView):
   
#     template_name=r'users/login.html'
#     form_class = UserLoginForm



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
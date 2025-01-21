from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomUserCreationForm, LogInUserForm, PasswordChangingForm
from django.views import generic
from django.contrib.auth.views import PasswordChangeView
from django.forms.utils import ErrorList
from django import forms
from .models import CustomUser
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'vtuapp/index.html')


# @login_required
# def logout_view(request):
#     logout(request)
#     return redirect('dashboard')
    

class SignUp(SuccessMessageMixin, generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'vtuapp/register.html'
    # success_messages = 'Please confirm your email address to complete the registration,activation link has been sent to your email, also check your email spam folder'
    success_message = 'You have successfully Registered, Kindly login to continue'

    def abc(self):
        ref = ""
        if "referal" in self.request.session:
            ref = (self.request.session["referal"])

        return ref

    def get_context_data(self, **kwargs):

        context = super(SignUp, self).get_context_data(**kwargs)
        context['referal_user'] = self.abc()

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        username = object.username
        email = object.email
        # object.email_verify = False
        # object.is_active = False
        user = object

        if CustomUser.objects.filter(username__iexact=object.username).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This username has been taken'])
            return self.form_invalid(form)

        elif CustomUser.objects.filter(email__iexact=object.email).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This email has been taken'])
            return self.form_invalid(form)
        elif CustomUser.objects.filter(Phone__iexact=object.Phone).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This Phone has been taken'])
            return self.form_invalid(form)

        elif not object.email.endswith(("@gmail.com",'@yahoo.com')):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList([u'We accept only valid gmail or yahoo mail account'])
            return self.form_invalid(form)

        elif object.referer_username:
            if CustomUser.objects.filter(username__iexact=object.referer_username).exists():
                referal_user = CustomUser.objects.get(
                    username__iexact=object.referer_username)

            else:
                object.referer_username = None

        form.save()
        return super(SignUp, self).form_valid(form)



class LogIn(generic.View):
    form_class = LogInUserForm
    template_name = 'registration/login.html'
    
    
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    
    def post(self, request):
        if request.method == 'POST':
            form = LogInUserForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                
                user = authenticate(username=username, password=password)
                
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, f'you are logged in as {username}')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Error')
            else:
                messages.error(request, "Username or Password is incorrect")
        form = LogInUserForm()
        return render(request, self.template_name, {'form': form})

@login_required(login_url='login')                    
def dashboard(request):
    return render(request, 'vtuapp/dashboard.html')


class PasswordChangeView(PasswordChangeView):
    form_class =PasswordChangingForm
    success_url = reverse_lazy('password_success')
    
    
def password_success(request):
    return render(request, 'registration/password_change_done.html')



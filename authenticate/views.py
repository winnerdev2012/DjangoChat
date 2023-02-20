from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings

from django.urls import reverse_lazy

from .forms import CustomAuthenticationForm, CustomSignUpForm

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm

class CustomLogoutView(LogoutView):
    redirect_field_name = settings.LOGOUT_REDIRECT_URL
    
class CustomSignUpView(CreateView):
    form_class = CustomSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
        
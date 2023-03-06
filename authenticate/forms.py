from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm

from django.utils.translation import gettext_lazy as _

from user.models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):    
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        

class CustomSignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text=_('Optional'))
    # last_name = forms.CharField(max_length=30, required=False, help_text=_('Optional'))
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = CustomUser
        fields = [
            'username', 
            # 'first_name', 
            # 'last_name', 
            'email',
            'gender', 
            'password1', 
            'password2', 
            ]

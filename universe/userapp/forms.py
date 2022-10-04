from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

class User_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class Profile_form(forms.ModelForm):
    profile_passport = forms.ImageField(required=False, label='Profile passport')
    particulars = forms.FileField(required=False, label='particular')
    class Meta:
        model = profile
        fields = [
            'gender',
            'phone',
            'address',
            'state',
            'nationality',
            'position',
            'marital_status',
            'staff',
            'profile_passport',
            'particulars',
            
            
        ]

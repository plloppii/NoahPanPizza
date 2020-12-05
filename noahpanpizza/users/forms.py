from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# User Register Form allows user to fill out form


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # default required

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# User Update Form allows user to update their fields


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Dedicated Profile Form used to update the image of the profile.


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

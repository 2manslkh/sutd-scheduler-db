from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Backend logic
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        # contains information about the class
        model = User
        fields = ['username', 'email', 'password1', 'password2']

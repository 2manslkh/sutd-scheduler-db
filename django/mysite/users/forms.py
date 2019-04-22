from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
# Backend logic


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        # contains information about the class
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("First name is required.")

        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("Last name is required.")

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

from django import forms
from django.contrib.auth import get_user_model


class UserRegistrationForm(forms.Form):
    model = get_user_model()

    email = forms.EmailField()
    fields = ['username', 'password1', 'password2', 'profile_picture', 'country', 'discord']
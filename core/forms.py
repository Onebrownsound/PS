from django import forms
from django.contrib.auth.models import User
from django.core import validators


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=30, validators=[validators.validate_email])
    firstname = forms.CharField(max_length=45)
    lastname = forms.CharField(max_length=45)
    socialmedianame = forms.CharField(max_length=45)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=100)
    password = forms.CharField(label='Password:', max_length=100, widget=forms.PasswordInput())

    class Meta:
        model = User

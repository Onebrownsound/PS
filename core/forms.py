from django import forms
from django.contrib.auth.models import User
from .models import Capsule


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=100)
    password = forms.CharField(label='Password:', max_length=100)

    class Meta:
        model = User
        fields = ('username', 'password')


class CapsuleForm(forms.ModelForm):

    time_delivery = forms.DateField(widget=forms.SelectDateWidget())
    author_twitter = forms.CharField(max_length=40, label='Your twitter ID:', help_text='Without @ Symbol',)
    target_twitter = forms.CharField(max_length=40, label='Target twitter ID:', help_text='Without @ Symbol')
    message = forms.CharField (max_length=1000)

    class Meta:
        model = Capsule
        fields = (
            'title', 'file', 'message', 'activation_type', 'delivery_condition', 'time_delivery', 'author_twitter',
            'target_twitter'
        )

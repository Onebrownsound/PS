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
    time_activation = forms.DateField(widget=forms.SelectDateWidget(),label='Select Activation Time')
    time_delivery = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Capsule
        fields = (
            'title',  'file', 'activation', 'time_activation', 'delivery', 'time_delivery',
        )

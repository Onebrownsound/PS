from django import forms
from django.contrib.auth.models import User
from .models import Capsule
from django.core import validators
from django.core.exceptions import ValidationError


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True, validators=[validators.validate_email])
    password = forms.CharField(widget=forms.PasswordInput())
    password_repeat = forms.CharField(widget=forms.PasswordInput())

    def clean_password_repeat(self):
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']
        if password != password_repeat:
            raise ValidationError('Passwords do not match')
        return password_repeat

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=100, required=True)
    password = forms.CharField(label='Password:', max_length=100, required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class CapsuleForm(forms.ModelForm):
    delivery_date = forms.DateField(widget=forms.SelectDateWidget())
    author_twitter = forms.CharField(max_length=40, label='Your twitter ID:', help_text='Without @ Symbol', )
    target_twitter = forms.CharField(max_length=40, label='Target twitter ID:', help_text='Without @ Symbol')
    message = forms.CharField(max_length=1000)
    target_email = forms.EmailField()
    class Meta:
        model = Capsule
        fields = (
            'title', 'file', 'message', 'activation_type', 'delivery_condition', "delivery_date", 'author_twitter',
            'target_twitter', 'target_email', 'target_firstname'
        )

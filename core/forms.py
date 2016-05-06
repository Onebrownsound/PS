from django import forms
from django.contrib.auth.models import User
from .models import Capsule
from django.core import validators
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, TabHolder, Tab, FormActions
import re


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(required=True, label='Nickname')
    email = forms.EmailField(required=True, validators=[validators.validate_email])
    password = forms.CharField(widget=forms.PasswordInput())
    password_repeat = forms.CharField(widget=forms.PasswordInput(), label='Password')

    def clean_password_repeat(self):
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']
        if password != password_repeat:
            raise ValidationError('Passwords do not match')
        return password_repeat

    def clean_username(self):
        lower_case_username = self.cleaned_data['username'].lower()
        return lower_case_username

    def clean_email(self):
        lower_case_email = self.cleaned_data['email'].lower()
        return lower_case_email

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    helper = FormHelper()
    helper.form_class = 'form-horizontal indigo'
    helper.form_method = 'POST'

    helper.label_class = 'col-lg-4'
    helper.field_class = 'col-lg-4'
    helper.layout = Layout(
        Field('username'),
        Field('email'),
        Field('password'),
        Field('password_repeat'),
        FormActions(
            Submit('submit', 'Submit', css_class='indigo btn btn-default'),
            Button('cancel', 'Cancel', css_class='indigo btn btn-default')
        ), )


class LoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=30, required=True)
    password = forms.CharField(label='Password:', max_length=40, required=True, widget=forms.PasswordInput())

    def clean_username(self):
        lower_case_username = self.cleaned_data['username'].lower()
        return lower_case_username

    class Meta:
        model = User
        fields = ('username', 'password')

    helper = FormHelper()
    helper.form_class = 'form-horizontal indigo'
    helper.form_method = 'POST'

    helper.label_class = 'col-lg-4'
    helper.field_class = 'col-lg-4'
    helper.layout = Layout(
        Field('username', ),
        Field('password', ),
        FormActions(
            Submit('submit', 'Submit', css_class='indigo btn btn-default'),
            Button('cancel', 'Cancel', css_class='indigo btn btn-default')
        )
    )


class CapsuleForm(forms.ModelForm):
    delivery_date = forms.DateField(widget=forms.SelectDateWidget())
    author_twitter = forms.CharField(max_length=40, label='Your twitter ID:')
    target_twitter = forms.CharField(max_length=40, label='Target twitter ID:')
    message = forms.CharField(max_length=1000)
    target_email = forms.EmailField()

    class Meta:
        model = Capsule
        fields = (
            'title', 'file', 'message', 'activation_type', 'delivery_condition', 'author_twitter',
            'target_twitter', 'target_email', 'target_firstname'
        )

    helper = FormHelper()
    helper.form_class = 'form-horizontal indigo'
    helper.form_method = 'POST'

    helper.label_class = 'col-lg-4'
    helper.field_class = 'col-lg-4'

    helper.layout = Layout(
        Field('title', ),
        Field('file', ),
        Field('message', ),
        Field('activation_type', ),
        Field('delivery_condition', ),
        Field('delivery_date'),
        PrependedText('author_twitter', '@', placeholder="username"),
        PrependedText('target_twitter', '@', placeholder="username"),
        Field('target_email'),
        Field('target_firstname', ),
        FormActions(
            Submit('submit', 'Submit', css_class='indigo btn btn-default'),
            Button('cancel', 'Cancel', css_class='indigo btn btn-default')
        ),

    )


class ClassifyForm(forms.Form):
    test_tweet = forms.CharField(max_length=200, label='Test Tweet:')

    def clean_test_tweet(self):
        cleaned_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ",
                                        self.cleaned_data['test_tweet']).split())
        return cleaned_tweet

    helper = FormHelper()
    helper.form_class = 'form-horizontal indigo'
    helper.form_method = 'POST'

    helper.label_class = 'col-lg-4'
    helper.field_class = 'col-lg-4'

    helper.layout = Layout(
        Field('test_tweet'),
        FormActions(
            Submit('submit', 'Submit', css_class='indigo btn btn-default'),
            Button('cancel', 'Cancel', css_class='indigo btn btn-default')
        ),
    )

# def validate_input(value):
#     if value == '' or value is None:
#         raise ValidationError(
#             ('%(value)s is not a valid input'),
#             params={'value': value},
#         )

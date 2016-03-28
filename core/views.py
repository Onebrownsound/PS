from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUserForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form['username'].value(), password=form['password'].value())
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'invalid':True})


    else:  # GET
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def home(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    return render(request, 'index.html', {'user': user})


@login_required()
def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        user_form = RegisterUserForm(data=request.POST)
        if user_form.is_valid():
            user = User.objects.create_user(user_form['username'].value(), user_form['email'].value(),
                                            user_form['password'].value())
            user.save()
            return redirect('home')
    else:
        user_form = RegisterUserForm()

    return render(request, 'register.html', {'user_form': user_form})

from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUserForm,LoginForm
from django.contrib.auth.models import User



# Create your views here.


def login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(user=form['username'], password=['password'])
            if user is not None and user.is_active():
                    login(request, user)
                    return HttpResponseRedirect('home')
            else:#login failed
                return HttpResponseRedirect('/login')
    else:#GET
        form = LoginForm()
        return render(request,'login.html',{'form':form})

def home(request):
    return render(request, 'index.html', {})


def register(request):
    # If it's a HTTP POST, we're interested in processing form data.
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

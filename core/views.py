from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUserForm, LoginForm, CapsuleForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Capsule, FUTURE_DELIVERY_DICT


'''View Functions Live Below'''


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'invalid': True})
    else:  # GET
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def home(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    return render(request, 'index.html', {'user': user})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def create_capsule_view(request):  # View for creating time capsules
    form = CapsuleForm()
    if request.method == 'POST':
        form = CapsuleForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)  # first save with a false commit to manually insert user id after
            form.owner = request.user  # sort of hackish but it works, hopefully find a better way later
            form.save()
            return redirect('home')  # TODO redirect to view which shows all of a users capsules
    return render(request, 'create_capsule.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(data=request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                            form.cleaned_data['password'])
            user.save()
            return redirect('login_view')
    else:
        form = RegisterUserForm()

    return render(request, 'register.html', {'form': form})


@login_required(login_url='login')
def display_capsules_view(request):
    if request.method == 'GET':
        capsules = Capsule.objects.filter(owner=request.user).order_by(
            '-created')  # get all capsules belonging to a particular user,recent first
        capsules = translate_delivery_condition(
            capsules)  # convert DB delivery notation to verbose string,aka 'SD' -> Specific Date In The Future

        return render(request, 'display_capsules.html', {'capsules': capsules})


'''Helper Functions Live Below'''


def translate_delivery_condition(ax):
    """
    Takes in a list of Capsule Model objects. Translates short delivery condition abbreviation to the verbose definition
    AKA 'M' -> 'Marriage". Import to note this does not save to the db. Make sure this never happens

    Args:
        ax:list of Capsule Model objects
    Output:
        ax: list of Capsule Model objects with delivery_condition expressed verbosely.
    """
    for data in ax:
        data.delivery_condition = FUTURE_DELIVERY_DICT[data.delivery_condition]
    return ax

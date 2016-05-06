from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUserForm, LoginForm, CapsuleForm, ClassifyForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Capsule
from .utils import translate_delivery_condition
from sklearn.externals import joblib
from post_classifier.post_classifier import INT_TO_CLASSIFICATION_STRING
from django.views.generic.edit import UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse

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


class CapsuleUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    redirect_field_name = ''
    model = Capsule
    form_class = CapsuleForm
    template_name = 'edit_capsule.html'
    success_url = '/capsules'

    # Here we override the UpdateViews get method. Do some authorization/model checking.
    # Then Resume the original UpdateViews.get() method, because we want that "original" behavior of UpdateView.get()
    def get(self, request, pk):
        try:
            requested_capsule = get_object_or_404(Capsule, pk=pk)
        except:
            raise Http404("We're Sorry No Capsule Matches That Query")
        if requested_capsule.owner_id != request.user.id:
            return HttpResponse('Unauthorized Access', status=403)
        return super(CapsuleUpdate, self).get(request)

    def post(self, request, pk, **kwargs):
        try:
            requested_capsule = get_object_or_404(Capsule, pk=pk)
        except:
            raise Http404("We're Sorry No Capsule Matches That Query")
        if requested_capsule.owner_id != request.user.id:
            return HttpResponse('Unauthorized Access', status=403)
        return super(CapsuleUpdate, self).post(request, pk, **kwargs)


class CapsuleDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    redirect_field_name = ''
    model = Capsule
    success_url = reverse_lazy('display_capsules_view')
    template_name = 'confirm_capsule_delete.html'
    form_class = CapsuleForm

    def get(self, request, pk):
        #TODO Make the template pretty it looks like garbo
        try:
            requested_capsule = get_object_or_404(Capsule, pk=pk)
        except:
            raise Http404("We're Sorry No Capsule Matches That Query")
        if requested_capsule.owner_id != request.user.id:
            return HttpResponse('Unauthorized Access', status=403)
        return render(request, self.template_name, {'pk': pk, 'capsule': requested_capsule})

    def post(self, request, pk):
        try:
            requested_capsule = get_object_or_404(Capsule, pk=pk)
        except:
            raise Http404("We're Sorry No Capsule Matches That Query")
        if requested_capsule.owner_id != request.user.id:
            return HttpResponse('Unauthorized Access', status=403)
        return super(CapsuleDelete, self).post(request, pk)


@login_required(login_url='login')
def display_capsules_view(request):
    if request.method == 'GET':
        capsules = Capsule.objects.filter(owner=request.user).order_by(
            '-created')  # get all capsules belonging to a particular user,recent first
        capsules = translate_delivery_condition(
            capsules)  # convert DB delivery notation to verbose string,aka 'SD' -> Specific Date In The Future

        return render(request, 'display_capsules.html', {'capsules': capsules})


@login_required(login_url='login')
def display_classify_view(request):
    classification = 'None'
    cleaned_tweet = 'None'
    if request.method == 'POST':
        form = ClassifyForm(data=request.POST)
        if form.is_valid():
            classifier = joblib.load('./post_classifier/classifier.pkl')
            predicted_classifications = classifier.predict([form.cleaned_data['test_tweet']])
            classification = INT_TO_CLASSIFICATION_STRING[predicted_classifications[0]]
            cleaned_tweet = form.cleaned_data['test_tweet']
    else:
        form = ClassifyForm()
        classification = 'None'
    return render(request, 'display_classification.html',
                  {'form': form, 'classification': classification, 'cleaned_tweet': cleaned_tweet})

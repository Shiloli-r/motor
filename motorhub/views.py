from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model, login, logout


from .forms import SearchForm, CustomerRegistrationForm, UserLoginForm, ContactForm, UserRegistrationForm
from .models import Manufacturers


# Create your views here.
def home(request):
    if request.method == 'POST':
        search = SearchForm(request.POST)
        if search.is_valid():
            return HttpResponseRedirect('index.html')
    else:
        search = SearchForm()
    method = request.method
    manufacturers = Manufacturers.objects.all()
    context = {
        'user_authenticated': request.user.is_authenticated,
        'user': request.user,
        'search': search,
        'method': method,
        'manufacturers': manufacturers,
    }
    return render(request, 'motorhub/index.html', context)


def car_search(request):
    if request.method == 'POST':
        search = SearchForm(request.POST)
        if search.is_valid():
            return HttpResponseRedirect('index.html')
    else:
        search = SearchForm()
    method = request.method

    context = {
        'search': search,
        'method': method,

    }
    return render(request, 'car_search.html', context)


def sign_up(request):
    next = request.GET.get('next')
    # signup form
    signup = CustomerRegistrationForm(request.POST or None)
    # signup = UserRegistrationForm(request.POST or None)
    if signup.is_valid():
        user = signup.save(commit=False)
        password = signup.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            redirect(next)
        return HttpResponseRedirect('dashboard')

        # The contact Form
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            return HttpResponseRedirect('')
    else:
        contact_form = ContactForm()

    context = {
        'sign_up': signup,
        'contact_form': contact_form,
    }
    return render(request, 'motorhub/signup.html', context)


def login_view(request):
    next = request.GET.get('next')
    # login form
    if request.method == 'POST':
        log_in = UserLoginForm(request.POST)
        if log_in.is_valid():
            username = log_in.cleaned_data.get('username')
            password = log_in.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            if next:
                redirect(next)
            return HttpResponseRedirect('dashboard')
    else:
        log_in = UserLoginForm()

    # The contact Form
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            return HttpResponseRedirect('')
    else:
        contact_form = ContactForm()

    context = {
        'log_in': log_in,
        'contact_form': contact_form,
        # 'signup_form': signup_form,
    }
    return render(request, 'motorhub/login.html', context)


@login_required
def dashboard(request):
    context = {

    }
    return render(request, 'motorhub/dashboard.html', context)


def about(request):
    context = {

    }
    return render(request, 'motorhub/about.html', context)


def settings(request):
    context = {

    }
    return render(request, 'motorhub/settings.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')

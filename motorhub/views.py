from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import SearchForm, CustomerForm, UserLoginForm, ContactForm
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


def login(request):
    # login form
    if request.method == 'POST':
        log_in = UserLoginForm(request.POST)
        if log_in.is_valid():
            return HttpResponseRedirect('/')
    else:
        log_in = UserLoginForm()

    # The signup Form
    if request.method == 'POST':
        signup_form = CustomerForm(request.POST)
        if signup_form.is_valid():
            return HttpResponseRedirect('/')
    else:
        signup_form = CustomerForm()

    # The contact Form
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            return HttpResponseRedirect('')
    else:
        contact_form = ContactForm()

    method = request.method

    context = {
        'log_in': log_in,
        'method': method,
        'contact_form': contact_form,
        'signup_form': signup_form,
    }
    return render(request, 'motorhub/login.html', context)


def dashboard(request):
    context={

    }
    return render(request, 'motorhub/dashboard.html', context)


def about(request):
    context={

    }
    return render(request, 'motorhub/about.html', context)


def settings(request):
    context = {

    }
    return render(request, 'motorhub/settings.html', context)
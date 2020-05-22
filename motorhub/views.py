from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import SearchForm, CustomerForm
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
    context = {

    }
    return render(request, 'motorhub/login.html', context)

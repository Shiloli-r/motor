from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import SearchForm


# Create your views here.
def home(request):
    return render(request, 'base.html')


def get_name(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/index.html')
    else:
        form = SearchForm()
    return render(request, 'base.html', {"form": form})

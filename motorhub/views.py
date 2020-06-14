from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model, login, logout

from .forms import SearchForm, CustomerRegistrationForm, UserLoginForm, ContactForm, UserRegistrationForm
from .models import Manufacturers, Cars


# Create your views here.
def home(request):
    search = SearchForm()
    method = request.method
    manufacturers = Manufacturers.objects.all()
    if request.GET:
        cars = Cars.objects.get(id=None, **request.GET)
    else:
        cars = Cars.objects.all()
    context = {
        'user_authenticated': request.user.is_authenticated,
        'user': request.user,
        'search': search,
        'method': method,
        'manufacturers': manufacturers,
        'cars': cars,
        'GET': request.GET,
    }
    return render(request, 'motorhub/index.html', context)


def view_car(request, id):
    car = Cars.objects.get(id=id)
    features = car.__dict__.values()
    fields = car._meta.get_fields()
    # dictonary = car.__dict__
    context = {
        'user_authenticated': request.user.is_authenticated,
        'car': car,
        'features': features,
        'fields': fields,
    }
    return render(request, 'motorhub/view_car.html', context)


def payment(request):
    context = {

    }
    return render(request, 'motorhub/payment.html', context)


def car_search(request):
    manufacturer = request.GET.get('manufacturer')
    body_type = request.GET.get('body_type')
    sub_body_type = request.GET.get('sub_body_type')
    steering = request.GET.get('steering')
    transmission = request.GET.get('transmission')
    fuel = request.GET.get('fuel')
    color = request.GET.get('color')
    loading_capacity = request.GET.get('loading_capacity')
    body_length = request.GET.get('body_length')
    grill_guard = request.GET.get('grill_guard')
    rear_spoiler = request.GET.get('rear_spoiler')
    anti_lock_brake_system = request.GET.get('anti_lock_brake_system')
    leather_seats = request.GET.get('leather_seats')
    sun_roof = request.GET.get('sun_roof')
    navigation = request.GET.get('navigation')
    tv = request.GET.get('tv')
    alloy_wheels = request.GET.get('alloy_wheels')
    power_steering = request.GET.get('power_steering')
    dual_air_bags = request.GET.get('dual_air_bags')
    back_tire = request.GET.get('back_tire')
    power_windows = request.GET.get('power_windows')
    fog_lights = request.GET.get('fog_lights')
    roof_rails = request.GET.get('roof_rails')
    method = request.method

    context = {
        'GET': request.GET,
        'request': request,
        'method': method,
        'manufacturer': manufacturer,
        'body_type': body_type,
        'sub_body_type': sub_body_type,
        'steering': steering,
        'transmission': transmission,
        'fuel': fuel,
        'color': color,
        'loading_capacity': loading_capacity,
        'body_length': body_length,
        'grill_guard': grill_guard,
        'rear_spoiler': rear_spoiler,
        'anti_lock_brake_system': anti_lock_brake_system,
        'leather_seats': leather_seats,
        'sun_roof': sun_roof,
        'navigation': navigation,
        'tv': tv,
        'alloy_wheels': alloy_wheels,
        'power_steering': power_steering,
        'dual_air_bags': dual_air_bags,
        'back_tire': back_tire,
        'power_windows': power_windows,
        'fog_lights': fog_lights,
        'roof_rails': roof_rails,
    }
    return render(request, 'motorhub/index.html', context)


def search_result(request):
    pass


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

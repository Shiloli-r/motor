from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model, login, logout

from .forms import SearchForm, CustomerRegistrationForm, UserLoginForm, ContactForm, UserRegistrationForm
from .models import Manufacturers, Cars, Cart, Customers


# Create your views here.
def home(request):
    search = SearchForm()
    manufacturers = Manufacturers.objects.all()
    manufacturer_ = request.GET.get('manufacturer_')
    id_ = request.GET.get('id')
    cart_items = Cart.objects.all()

    if id_:
        if request.user.is_authenticated:
            dictionary = {
                'car': Cars.objects.get(id=id_),
                'customer': Customers.objects.get(id=request.user.id),
            }
            Cart.objects.create(**dictionary)
            return HttpResponseRedirect('.')
        else:
            return HttpResponseRedirect('login')
    elif manufacturer_:
        cars = Cars.objects.filter(manufacturer__manufacturer=manufacturer_)
    elif request.GET:
        qs = Cars.objects.all()
        for item in request.GET:
            entry = request.GET.get(str(item))
            if entry != '' and entry is not None:
                print(item, entry)
                if entry == 'on':
                    entry = True
                if item == 'manufacturer':
                    qs = Cars.objects.filter(manufacturer__manufacturer=entry)
                else:
                    dictionary = {
                        item: entry,
                    }
                    qs = qs.filter(**dictionary)
        cars = qs
    else:
        cars = Cars.objects.all()
        for item in cart_items:
            cars = cars.exclude(id=item.car.id)

    context = {
        'user_authenticated': request.user.is_authenticated,
        'user': request.user,
        'search': search,
        'manufacturers': manufacturers,
        'cars': cars,
    }
    return render(request, 'motorhub/index.html', context)


def view_car(request, id):
    car = Cars.objects.get(id=id)
    features = car.__dict__.values()
    fields = car._meta.get_fields()
    context = {
        'user_authenticated': request.user.is_authenticated,
        'car': car,
        'features': features,
        'fields': fields,
    }
    return render(request, 'motorhub/view_car.html', context)


def payment(request, cart_item_id=None):
    cart_items = Cart.objects.all()
    total_price = 0
    for item in cart_items:
        total_price += item.car.price
    if request.method == 'GET':
        cart_id = request.GET.get('cart_item_id', '')
        if cart_id:
            print(cart_id)
        else:
            print('Cart Id not found')
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'motorhub/payment.html', context)


def delete_cart(request, id):
    cart_item = Cart.objects.get(id=id).delete()
    return redirect('payment')


def car_search(request):

    context = {

    }
    return render(request, 'motorhub/index.html', context)


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

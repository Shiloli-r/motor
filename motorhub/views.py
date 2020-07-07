from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


from .forms import SearchForm, CustomerRegistrationForm, UserLoginForm, ContactForm
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
                'customer': Customers.objects.get(user=request.user),
            }
            Cart.objects.create(**dictionary)
            return HttpResponseRedirect('.')
        else:
            return redirect('login')
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
        if request.user.is_authenticated:
            cars = Cars.objects.all()
            for item in cart_items:
                cars = cars.exclude(id=item.car.id)
        else:
            cars = Cars.objects.all()

    context = {
        'user_authenticated': request.user.is_authenticated,
        'user': request.user,
        'search': search,
        'manufacturers': manufacturers,
        'cars': cars,

    }
    return render(request, 'motorhub/index.html', context)


def view_car(request, id):
    search = SearchForm()
    car = Cars.objects.get(id=id)

    context = {
        'user_authenticated': request.user.is_authenticated,
        'car': car,
        'search': search,
    }
    return render(request, 'motorhub/view_car.html', context)


@login_required
def payment(request):
    search = SearchForm()
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
        'search': search,
    }
    return render(request, 'motorhub/payment.html', context)


@login_required
def delete_cart(request, id):
    Cart.objects.get(id=id).delete()
    return redirect('payment')


@login_required
def delete_cart(request, id):
    Cart.objects.get(id=id).delete()
    return redirect('dashboard')


def car_search(request):

    context = {

    }
    return render(request, 'motorhub/index.html', context)


def sign_up(request):
    # signup form
    message = ''
    signup = CustomerRegistrationForm()
    # signup = UserRegistrationForm(request.POST or None)
    if request.method == 'POST':
        signup = CustomerRegistrationForm(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        id_number = request.POST['id_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        country = request.POST['country']
        city = request.POST['city']
        street = request.POST['street']
        postal_code = request.POST['postal_code']
        profile_picture = request.FILES.get('profile_picture')

        if password != confirm_password:
            message = 'The Two Passwords Do Not Match'
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            message = "The Username is Already Taken"
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            message = "The Email is Already Registered"
        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
        user.save()
        authenticate(username=user.username, password=user.password)
        login(request, user)
        instance = User.objects.get(id=user.id)
        customer = Customers.objects.create(user=instance, id_number=id_number, country=country, street=street,
                                            city=city, postal_code=postal_code, profile_picture=profile_picture)

        customer.save()
        subject = "Welcome to Motorhub - Confirm Email"
        message = "Click on this link to verify your email http://r8nn1e.pythonanywhere.com/{}/verify".format(user.username)
        sender_email = 'ocdgroup1@gmail.com'
        receiver_email = email
        send_mail(subject, message, sender_email, [receiver_email], fail_silently=True,)
        return redirect(dashboard)

        # The contact Form
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            return HttpResponseRedirect('')
    else:
        contact_form = ContactForm()

    context = {
        'sign_up': signup,
        'message': message,
        'contact_form': contact_form,
    }
    return render(request, 'motorhub/signup.html', context)


def verify(request, username):
    user = User.objects.get(username=username)
    authenticate(username=user.username, password=user.password)
    login(request, user)
    user.customers.email_verfied = True
    user.customers.save()
    return redirect(dashboard)


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
    search = SearchForm()
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
        'search': search,
        'cart_items': cart_items,
        'total_price': total_price,
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

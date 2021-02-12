from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum


from .forms import SearchForm, CustomerRegistrationForm, UserLoginForm, ContactForm
from .models import Manufacturers, Cars, Cart, Customers, Orders, Notifications

import stripe
stripe.api_key = "sk_test_51H3WhAK9AbYX1AmlB674uhUsbFrrcgju9ijRLuRgq5K1idYgxr8GO1yLEQVgReYMqvaxToNqHCIKyHceFcLrEyrS006benXp26"


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
        ordered = Orders.objects.all()
        for order in ordered:
            cars = cars.exclude(id=order.car.id)
        if request.user.is_authenticated:
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
    user = User.objects.get(username=request.user)
    cart_items = Cart.objects.all()
    cart_items = cart_items.filter(customer=user.customers)
    total_price = cart_items.aggregate(Sum('car__price'))['car__price__sum']
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
    return render(request, 'motorhub/index.html')


def sign_up(request):
    # signup form

    signup = CustomerRegistrationForm(request.POST or None)
    # signup = UserRegistrationForm(request.POST or None)
    if signup.is_valid():
        first_name = signup.cleaned_data.get('first_name')
        last_name = signup.cleaned_data.get('last_name')
        username = signup.cleaned_data.get('username')
        email = signup.cleaned_data.get('email')
        id_number = signup.cleaned_data.get('id_number')
        password = signup.cleaned_data.get('password')
        country = signup.cleaned_data.get('country')
        city = signup.cleaned_data.get('city')
        street = signup.cleaned_data.get('street')
        postal_code = signup.cleaned_data.get('postal_code')
        profile_picture = request.FILES.get('profile_picture')

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
        user.save()
        authenticate(username=user.username, password=user.password)
        login(request, user)
        instance = User.objects.get(id=user.id)
        customer = Customers.objects.create(user=instance, id_number=id_number, country=country, street=street,
                                            city=city, postal_code=postal_code, profile_picture=profile_picture)

        customer.save()
        subject = "Welcome to Motorhub - Confirm Email"
        message = "Click on this link to verify your email https://r8nn1e.pythonanywhere.com/{}/verify".format(user.username)
        sender_email = 'ocdgroup1@gmail.com'
        receiver_email = email
        send_mail(subject, message, sender_email, [receiver_email], fail_silently=True,)
        note = "A confirmation link has been sent to {} ".format(user.email)
        notification = Notifications.objects.create(customer=customer, subject="Verify Your Email", notification=note)
        notification.save()
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
        'contact_form': contact_form,
    }
    return render(request, 'motorhub/signup.html', context)


def verify(request, username):
    user = User.objects.get(username=username)
    authenticate(username=user.username, password=user.password)
    login(request, user)
    user.customers.email_verfied = True
    user.customers.save()
    note = "Your Email address {} has been verified".format(user.email)
    notification = Notifications.objects.create(customer=user.customers, subject='Email Verifed', notification=note)
    notification.save()
    return redirect(dashboard)


def login_view(request):
    next = request.GET.get('next')
    # login form
    log_in = UserLoginForm(request.POST or None)
    if log_in.is_valid():
        username = log_in.cleaned_data.get('username')
        password = log_in.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            redirect(next)
        return redirect('dashboard')

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
    }
    return render(request, 'motorhub/login.html', context)


@login_required
def dashboard(request):
    user = User.objects.get(username=request.user)
    search = SearchForm()
    cart_items = Cart.objects.all()
    cart_items = cart_items.filter(customer=user.customers)
    notifications = Notifications.objects.all()
    notifications = notifications.filter(customer=user.customers)
    notifications_count = notifications.filter(read=False).count
    orders = Orders.objects.all()
    orders = orders.filter(customer=user.customers)
    pending = orders.filter(completed=False)
    completed = orders.filter(completed=True)

    total_price = 0
    for item in cart_items:
        total_price += item.car.price
    if request.method == 'GET':
        cart_id = request.GET.get('cart_item_id', '')
    context = {
        'search': search,
        'cart_items': cart_items,
        'total_price': total_price,
        'notifications_count': notifications_count,
        'notifications': notifications,
        'completed': completed,
        'pending': pending,
    }
    return render(request, 'motorhub/dashboard.html', context)


def about(request):
    return render(request, 'motorhub/about.html')


@login_required
def charge(request):
    cart_items = Cart.objects.all()
    total_price = cart_items.aggregate(Sum('car__price'))['car__price__sum']
    user = User.objects.get(username=request.user)
    full_name = '{} {}'.format(user.first_name, user.last_name)
    email = user.email
    if request.method == 'POST':
        if not full_name or full_name == '':
            full_name = request.POST['name']
        if not email or email == '':
            email = request.POST['name']
        customer = stripe.Customer.create(
            name=full_name,
            email=email,
            source=request.POST['stripeToken']
        )

        stripe.Charge.create(
            customer=customer,
            amount=total_price*100,
            currency='usd',
            description='Purchased Car'
        )
        for item in cart_items:
            order = Orders.objects.create(customer=user.customers, car=item.car)
            order.save()
            item.delete()
            note = 'Payment for {} was successful'.format(item.car)
            notification = Notifications.objects.create(customer=user.customers, subject="Payment Successful", notification=note)
            notification.save()
    return redirect(dashboard)


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def complete(request, id):
    order = Orders.objects.get(id=id)
    if request.method == 'GET':
        checked = request.GET.get('completed')
        comments = request.GET.get('comments')
        if comments:
            order.comments = comments
            order.save()
        if checked:
            order.completed = True
            order.save()
            return redirect(dashboard)
    context = {
        "order": order,
    }
    return render(request, 'motorhub/complete.html', context)

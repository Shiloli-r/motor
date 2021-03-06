from django.db import models
from django.contrib.auth.models import User
# noinspection PyUnresolvedReferences
from django_countries.fields import CountryField

from datetime import datetime, timedelta


# Create your models here.
class Manufacturers(models.Model):
    manufacturer = models.CharField(max_length=100)
    logo = models.ImageField()

    def __str__(self):
        return self.manufacturer

    class Meta:
        verbose_name_plural = 'Manufacturers'


class Cars(models.Model):
    BODY_TYPE = [
        ("Sedan", "Sedan"), ("Coupe", "Coupe"), ("Hatchback", "Hatchback"), ("SUV", "SUV"), ("Pick Up", "Pick Up"),
        ("Van", "Van"), ("Mini Van", "Mini Van"), ("Wagon", "Wagon"), ("Convertible", "Convertible"), ("Bus", "Bus"),
        ("Truck", "Truck"), ("Heavy Equipment", "Heavy Equipment"),
        ("Agricultural Equipment", "Agricultural Equipment"),
    ]
    SUB_BODY_TYPE = [
        ("Flat Body", "Flat Body"), ("Crane", "Crane"), ("Dump", "Dump"), ("Loader", "Loader"), ("Chassis", "Chassis"),
        ("Garbage Truck", "Garbage Truck"), ("High Elevation Work Truck", "High Elevation Work Truck"),
        ("Self", "Self"), ("Fork Lift", "Fork Lift"), ("Mini Excavator", "Mini Excavator"), ("Dozer", "Dozer"),
        ("Excavator", "Excavator"), ("Rollers", "Graders"), ("Finishers", "Finishers"), ("Attachments", "Attachments"),
        ("Box", "Box"), ("Compressor", "Compressor"), ("Double Cabin", "Double Cabin"), ("Tractor", "Tractor"),
    ]
    STEERING = [
        ("Right Hand Drive", "Right Hand Drive"), ("Left Hand Drive", "Left Hand Drive"),
    ]
    TRANSMISSION = [
        ("Automatic", "Automatic"), ("Manual", "Manual"), ("Smoother", "Smoother"), ("Semi AT", "Semi AT"),
        ("Inomat", "Inomat"), ("Duonic", "Duonic"), ("Escot", "Escot"), ("Proshift", "Proshift"),
    ]
    FUEL = [
        ("Petrol", "Petrol"), ("Diesel", "Diesel"), ("LPG", "LPG"), ("Electric Vehicle", "Electric Vehicle"),
        ("Hybrid(Petrol)", "Hybrid(Petrol)"), ("Hybrid(Diesel)", "Hybrid(Diesel)"),
    ]
    COLOUR = [
        ("Beige", "Beige"), ("Black", "Black"), ("Blue", "Blue"), ("Cream", "Cream"), ("Gold", "Gold"),
        ("Gray", "Gray"),
        ("Green", "Green"), ("Orange", "Orange"), ("Pearl", "Pearl"), ("Pink", "Pink"), ("Purple", "Purple"),
        ("Red", "Red"), ("Rose", "Rose"), ("Silver", "Silver"), ("White", "White"), ('White', 'White'),
        ('Yellow', 'Yellow'), ('Brown', 'Brown'),
    ]
    LOADING_CAPACITY = [
        ("Under 1 ton", "Under 1 ton"), ("1 to 2 ton", "1 to 2 ton"), ("2 to 2.5 ton", "2 to 2.5 ton"),
        ("2.5 to 3 ton", "2.5 to 3 ton"), ("3 to 4 ton", "3 to 4 ton"), ("4 to 5 ton", "4 to 5 ton"),
        ("4 to 5 ton", "4 to 5 ton"), ("5 to 6 ton", "5 to 6 ton"), ("6 to 7 ton", "6 to 7 ton"),
        ("7 to 8 ton", "7 to 8 ton"), ("8 to 9 ton", "8 to 9 ton"), ("9 to 10 ton", "9 to 10 ton"),
        ("Over 10 ton", "Over 10 ton"),
    ]
    BODY_LENGTH = [
        ("Under 3400mm", "Under 3400mm"), ("3400 to 4000mm", "3400 to 4000mm"), ("4000 to 4500mm", "4000 to 4500mm"),
        ("4500 to 4700mm", "4500 to 4700mm"), ("4700 to 4795mm", "4700 to 4795mm"),
        ("4795 to 5000mm", "4795 to 5000mm"),
        ("5000 to 5100mm", "5000 to 5100mm"), ("Over 5100mm", "Over 5100mm"),
    ]
    manufacturer = models.ForeignKey(Manufacturers, on_delete=models.CASCADE)
    body_type = models.CharField(max_length=100, choices=BODY_TYPE)
    sub_body_type = models.CharField(max_length=100, choices=SUB_BODY_TYPE)
    steering = models.CharField(max_length=80, choices=STEERING)
    transmission = models.CharField(max_length=80, choices=TRANSMISSION)
    fuel = models.CharField(max_length=80, choices=FUEL)
    color = models.CharField(max_length=30, choices=COLOUR)
    loading_capacity = models.CharField(max_length=100, choices=LOADING_CAPACITY)
    body_length = models.CharField(max_length=100, choices=BODY_LENGTH)
    image = models.ImageField()
    price = models.IntegerField(default=5000)
    airbag = models.BooleanField(default=True)
    grill_guard = models.BooleanField(default=False)
    rear_spoiler = models.BooleanField(default=False)
    anti_lock_brake_system = models.BooleanField(default=True)
    leather_seats = models.BooleanField(default=True)
    sun_roof = models.BooleanField(default=False)
    air_conditioner = models.BooleanField(default=True)
    navigation = models.BooleanField(default=True)
    tv = models.BooleanField(default=False)
    alloy_wheels = models.BooleanField(default=False)
    power_steering = models.BooleanField(default=True)
    dual_air_bags = models.BooleanField(default=True)
    back_tire = models.BooleanField(default=True)
    power_windows = models.BooleanField(default=False)
    fog_lights = models.BooleanField(default=True)
    roof_rails = models.BooleanField(default=False)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    image4 = models.ImageField(null=True, blank=True)
    image5 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return "{} {} - {}, {}".format(self.manufacturer, self.body_type, self.sub_body_type, self.steering)

    class Meta:
        verbose_name_plural = "Cars"


class Customers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.IntegerField()
    country = CountryField()
    street = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    profile_picture = models.ImageField(null=True, blank=True)
    email_verfied = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name_plural = "Customers"


class Orders(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now=True)
    date_due = models.DateField(default=datetime.now()+timedelta(days=7))
    completed = models.BooleanField(default=False)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{} ordered {}".format(self.car, self.date_ordered)

    class Meta:
        verbose_name_plural = "Orders"


class Contact(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    email = models.EmailField()
    date = models.DateTimeField()
    read = models.BooleanField(default=False)


class Cart(models.Model):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.customer, self.car)


class Notifications(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    subject = models.CharField(max_length=250)
    notification = models.CharField(max_length=255)
    read = models.BooleanField(default=False)

    def __str__(self):
        return '{}: {}'.format(self.subject, self.notification)

    class Meta:
        verbose_name_plural = "Notifications"


from django.db import models
# noinspection PyUnresolvedReferences
from django_countries.fields import CountryField


# Create your models here.
class Cars(models.Model):
    CAR_MAKE = [
        ("Toyota", "Toyota"), ("Nissan", "Nissan"), ("Honda", "Honda"), ("Mazda", "Mazda"), ("Jeep", "Jeep"),
        ("Mitsubishi", "Mitsubishi"), ("Suzuki", "Suzuki"), ("Subaru", "Subaru"), ("BMW", "BMW"), ("Dodge", "Dodge"),
        ("Mercedes", "Mercedes"), ("Volkswagen", "Volkswagen"), ("Audi", "Audi"), ("Ford", "Ford"), ("Mini", "Mini"),
        ("Lexus", "Lexus"), ("Land Rover", "Land Rover"), ("Hyundai", "Hyundai"), ("Volvo", "Scania"),
        ("Peugeot", "Peugeot"), ("Renault", "Renault"), ("Jaguar", "Jaguar"), ("Isuzu", "Isuzu"), ("Audi", "Audi"),
    ]
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
        ("Red", "Red"), ("Rose", "Rose"), ("Silver", "Silver"), ("White", "White"),
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
    make = models.CharField(max_length=100, choices=CAR_MAKE)
    body_type = models.CharField(max_length=100, choices=BODY_TYPE)
    sub_body_type = models.CharField(max_length=100, choices=SUB_BODY_TYPE)
    steering = models.CharField(max_length=80, choices=[
        ("Right Hand Drive", "Right Hand Drive"), ("Left Hand Drive", "Left Hand Drive"),
    ])
    transmission = models.CharField(max_length=80, choices=TRANSMISSION)
    fuel = models.CharField(max_length=80, choices=FUEL)
    color = models.CharField(max_length=30, choices=COLOUR)
    loading_capacity = models.CharField(max_length=100, choices=LOADING_CAPACITY)
    body_length = models.CharField(max_length=100, choices=BODY_LENGTH)
    airbag = models.BooleanField()
    grill_guard = models.BooleanField()
    rear_spoiler = models.BooleanField()
    anti_lock_brake_system = models.BooleanField()
    leather_seats = models.BooleanField()
    sun_roof = models.BooleanField()
    air_conditioner = models.BooleanField()
    navigation = models.BooleanField()
    tv = models.BooleanField()
    alloy_wheels = models.BooleanField()
    power_steering = models.BooleanField()
    dual_air_bags = models.BooleanField()
    back_tire = models.BooleanField()
    power_windows = models.BooleanField()
    fog_lights = models.BooleanField()
    roof_rails = models.BooleanField()

    def __str__(self):
        return "{} {} - {}, {}".format(self.make, self.body_type, self.sub_body_type, self.steering)

    class Meta:
        verbose_name_plural = "Cars"


class Customers(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=500)
    country = CountryField()
    street = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = "Customers"


class Orders(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now=True)
    date_due = models.DateTimeField(auto_now=False)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{} -> {} ordered {}".format(self.customer, self.car, self.date_ordered)

    class Meta:
        verbose_name_plural = "Orders"

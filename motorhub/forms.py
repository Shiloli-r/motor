from django.forms import ModelForm
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from django_countries import countries

from motorhub.models import Cars, Contact, Manufacturers, Customers

BODY_TYPE = [('', ''),
             ("Sedan", "Sedan"), ("Coupe", "Coupe"), ("Hatchback", "Hatchback"), ("SUV", "SUV"), ("Pick Up", "Pick Up"),
             ("Van", "Van"), ("Mini Van", "Mini Van"), ("Wagon", "Wagon"), ("Convertible", "Convertible"),
             ("Bus", "Bus"),
             ("Truck", "Truck"), ("Heavy Equipment", "Heavy Equipment"),
             ("Agricultural Equipment", "Agricultural Equipment"),
             ]
SUB_BODY_TYPE = [('', ''),
                 ("Flat Body", "Flat Body"), ("Crane", "Crane"), ("Dump", "Dump"), ("Loader", "Loader"),
                 ("Chassis", "Chassis"),
                 ("Garbage Truck", "Garbage Truck"), ("High Elevation Work Truck", "High Elevation Work Truck"),
                 ("Self", "Self"), ("Fork Lift", "Fork Lift"), ("Mini Excavator", "Mini Excavator"), ("Dozer", "Dozer"),
                 ("Excavator", "Excavator"), ("Rollers", "Graders"), ("Finishers", "Finishers"),
                 ("Attachments", "Attachments"),
                 ("Box", "Box"), ("Compressor", "Compressor"), ("Double Cabin", "Double Cabin"), ("Tractor", "Tractor"),
                 ]
STEERING = [('', ''),
            ("Right Hand Drive", "Right Hand Drive"), ("Left Hand Drive", "Left Hand Drive"),
            ]
TRANSMISSION = [('', ''),
                ("Automatic", "Automatic"), ("Manual", "Manual"), ("Smoother", "Smoother"), ("Semi AT", "Semi AT"),
                ("Inomat", "Inomat"), ("Duonic", "Duonic"), ("Escot", "Escot"), ("Proshift", "Proshift"),
                ]
FUEL = [('', ''),
        ("Petrol", "Petrol"), ("Diesel", "Diesel"), ("LPG", "LPG"), ("Electric Vehicle", "Electric Vehicle"),
        ("Hybrid(Petrol)", "Hybrid(Petrol)"), ("Hybrid(Diesel)", "Hybrid(Diesel)"),
        ]
COLOUR = [('', ''),
          ("Beige", "Beige"), ("Black", "Black"), ("Blue", "Blue"), ("Cream", "Cream"), ("Gold", "Gold"),
          ("Gray", "Gray"),
          ("Green", "Green"), ("Orange", "Orange"), ("Pearl", "Pearl"), ("Pink", "Pink"), ("Purple", "Purple"),
          ("Red", "Red"), ("Rose", "Rose"), ("Silver", "Silver"), ("White", "White"),
          ]
LOADING_CAPACITY = [('', ''),
                    ("Under 1 ton", "Under 1 ton"), ("1 to 2 ton", "1 to 2 ton"), ("2 to 2.5 ton", "2 to 2.5 ton"),
                    ("2.5 to 3 ton", "2.5 to 3 ton"), ("3 to 4 ton", "3 to 4 ton"), ("4 to 5 ton", "4 to 5 ton"),
                    ("4 to 5 ton", "4 to 5 ton"), ("5 to 6 ton", "5 to 6 ton"), ("6 to 7 ton", "6 to 7 ton"),
                    ("7 to 8 ton", "7 to 8 ton"), ("8 to 9 ton", "8 to 9 ton"), ("9 to 10 ton", "9 to 10 ton"),
                    ("Over 10 ton", "Over 10 ton"),
                    ]
BODY_LENGTH = [('', ''),
               ("Under 3400mm", "Under 3400mm"), ("3400 to 4000mm", "3400 to 4000mm"),
               ("4000 to 4500mm", "4000 to 4500mm"),
               ("4500 to 4700mm", "4500 to 4700mm"), ("4700 to 4795mm", "4700 to 4795mm"),
               ("4795 to 5000mm", "4795 to 5000mm"),
               ("5000 to 5100mm", "5000 to 5100mm"), ("Over 5100mm", "Over 5100mm"),
               ]

User = get_user_model()


class Search(forms.Form):
    search = forms.CharField(max_length=150)


class SearchForm(forms.Form):
    manufacturer = forms.CharField(max_length=255, required=False)
    body_type = forms.ChoiceField(choices=BODY_TYPE, initial=None, required=False)
    sub_body_type = forms.ChoiceField(choices=SUB_BODY_TYPE, initial=None, required=False)
    steering = forms.ChoiceField(choices=STEERING, initial=None, required=False)
    transmission = forms.ChoiceField(choices=TRANSMISSION, initial=None, required=False)
    fuel = forms.ChoiceField(choices=FUEL, initial=None, required=False)
    color = forms.ChoiceField(choices=COLOUR, initial=None, required=False)
    loading_capacity = forms.ChoiceField(choices=LOADING_CAPACITY, initial=None, required=False)
    body_length = forms.ChoiceField(choices=BODY_LENGTH, initial=None, required=False)
    airbag = forms.BooleanField(required=False)
    grill_guard = forms.BooleanField(required=False)
    rear_spoiler = forms.BooleanField(required=False)
    anti_lock_brake_system = forms.BooleanField(required=False)
    leather_seats = forms.BooleanField(required=False)
    sun_roof = forms.BooleanField(required=False)
    air_conditioner = forms.BooleanField(required=False)
    navigation = forms.BooleanField(required=False)
    tv = forms.BooleanField(required=False)
    alloy_wheels = forms.BooleanField(required=False)
    power_steering = forms.BooleanField(required=False)
    dual_air_bags = forms.BooleanField(required=False)
    back_tire = forms.BooleanField(required=False)
    power_windows = forms.BooleanField(required=False)
    fog_lights = forms.BooleanField(required=False)
    roof_rails = forms.BooleanField(required=False)


class CustomerRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    id_number = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
   # country = CountryField(blank_label='Kenya').formfield()
    country = forms.ChoiceField(widget=CountrySelectWidget, choices=countries, label='Country')
    street = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    postal_code = forms.CharField(max_length=100)
    profile_picture = forms.ImageField(allow_empty_file=True)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("The 2 Passwords Do Not Match")
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            forms.ValidationError("This username is taken")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            forms.ValidationError("This email is already registered")

        return super(CustomerRegistrationForm, self).clean(*args, **kwargs)


class UserRegistrationForm(ModelForm):
    email = forms.EmailField(label='Email Address')
    email2 = forms.EmailField(label='Confrim Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if email != email2:
            raise forms.ValidationError("Emails Do not Match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email is already in use")
        return super(UserRegistrationForm, self).clean(*args, **kwargs)


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")
            if not user.is_active:
                raise forms.ValidationError("User is not Active")

        return super(UserLoginForm, self).clean(*args, **kwargs)


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['subject', 'message', 'email']

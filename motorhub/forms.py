from django.forms import ModelForm
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

from motorhub.models import Cars, Contact

User = get_user_model()


class Search(forms.Form):
    search = forms.CharField(max_length=150)


class SearchForm(ModelForm):
    manufacturer = forms.CharField(max_length=255)
    body_type = forms.ChoiceField(choices=Cars.BODY_TYPE)
    sub_body_type = forms.ChoiceField(choices=Cars.SUB_BODY_TYPE)
    steering = forms.ChoiceField(choices=Cars.STEERING)
    transmission = forms.ChoiceField(choices=Cars.TRANSMISSION)
    fuel = forms.ChoiceField(choices=Cars.FUEL)
    color = forms.ChoiceField(choices=Cars.COLOUR)
    loading_capacity = forms.ChoiceField(choices=Cars.LOADING_CAPACITY)
    body_length = forms.ChoiceField(choices=Cars.BODY_LENGTH)

    class Meta:
        model = Cars
        fields = '__all__'


class CustomerRegistrationForm(ModelForm):
    # first_name = forms.CharField(max_length=150)
    # last_name = forms.CharField(max_length=150)
    # id_number = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    # country = CountryField(blank_label='Kenya').formfield()
    # street = forms.CharField(max_length=255)
    # city = forms.CharField(max_length=255)
    # postal_code = forms.CharField(max_length=100)

    # profile_picture = forms.ImageField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        # fields = ['first_name', 'last_name', 'username', 'id_number', 'email', 'password', 'confirm_password',
        #           'country', 'street', 'city', 'postal_code']
        # widgets = {'country': CountrySelectWidget()
        #            }

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("The 2 Passwords Do Not Match")
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            forms.ValidationError("This username is taken")

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

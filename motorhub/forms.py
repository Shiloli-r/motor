from django.forms import ModelForm  # , Textarea
from django import forms

from motorhub.models import Cars, Customers, Contact


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


class CustomerForm(ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'
        exclude = ['user']


class UserLoginForm(ModelForm):
    password = forms.PasswordInput()

    class Meta:
        model = Customers
        fields = ['email', 'password']


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['subject', 'message', 'email']

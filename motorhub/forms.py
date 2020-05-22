from django.forms import ModelForm  # , Textarea
from django import forms
from motorhub.models import Cars, Customers


class Search(forms.Form):
    search = forms.CharField(max_length=150)


class SearchForm(ModelForm):
    make = forms.ChoiceField(choices=Cars.CAR_MAKE)
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

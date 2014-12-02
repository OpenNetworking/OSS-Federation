from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Issuer, Color, Address

class AddressCreationForm(ModelForm):
    class Meta:
        model = Address
        exclude = ('issuer',)

class AddressInputForm(forms.Form):
    address = forms.CharField(max_length=50)

class IssuerCreationForm(ModelForm):
    class Meta:
        model = Issuer
        exclude = ('user', 'account_name',)

class IssuerUpdateForm(ModelForm):
    class Meta:
        model = Issuer
        exclude = ('user', )

class ColorCreationForm(ModelForm):
    class Meta:
        model = Color
        exclude = ('issuer', 'color_id', 'address', 'is_confirmed')


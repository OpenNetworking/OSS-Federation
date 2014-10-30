from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Issuer, Color, ActiveAddress

class ActiveAddressCreationForm(ModelForm):
    class Meta:
        model = ActiveAddress


class IssuerCreationForm(ModelForm):
    class Meta:
        model = Issuer
        exclude = ('user',)


class ColorCreationForm(ModelForm):
    class Meta:
        model = Color
        exclude = ('issuer', 'color_number', 'current_address')


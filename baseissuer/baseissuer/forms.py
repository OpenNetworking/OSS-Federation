from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy
from bitcoinrpc import connect_to_local

from .models import BaseIssuer, Color, Address

def is_valid_address(address):
    rpc = connect_to_local()
    if address:
        return rpc.validateaddress(address).isvalid
    else:
        return False

class AddressCreationForm(ModelForm):
    class Meta:
        model = Address
        exclude = ('issuer',)

class AddressInputForm(forms.Form):
    error_messages = {
        'address_not_valid': "The address is not a valid gcoin address.",
    }
    address = forms.CharField(label=ugettext_lazy("Address"), max_length=50)

    def clean_address(self):
        address = self.cleaned_data.get("address")

        if not is_valid_address(address):
            raise forms.ValidationError(
                    self.error_messages['address_not_valid'],
                    code='address_not_valid',
                    )

        return address

class BaseIssuerCreationForm(ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    email = forms.CharField(label=ugettext_lazy('Email Address'))
    name = forms.CharField(label=ugettext_lazy('Name'))
    url = forms.CharField(label=ugettext_lazy('Url'))
    password1 = forms.CharField(label=ugettext_lazy("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=ugettext_lazy("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=ugettext_lazy("Enter the same password as above, for verification."))

    class Meta:
        model = BaseIssuer
        fields = ('email', 'name', 'url')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
            return password2

    def save(self, commit=True):
        baseissuer = super(BaseIssuerCreationForm, self).save()
        baseissuer.set_password(self.cleaned_data['password1'])
        if commit:
            baseissuer.save()
        return baseissuer

class BaseIssuerUpdateForm(ModelForm):
    class Meta:
        model = BaseIssuer
        exclude = ('user', )

class ColorCreationForm(ModelForm):
    color_name = forms.CharField(label=ugettext_lazy('Color Name'))

    class Meta:
        model = Color
        exclude = ('issuer', 'color_id', 'address', 'is_confirmed', 'is_confirming')


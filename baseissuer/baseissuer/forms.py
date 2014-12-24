from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import BaseIssuer, Color, Address

class AddressCreationForm(ModelForm):
    class Meta:
        model = Address
        exclude = ('issuer',)

class AddressInputForm(forms.Form):
    address = forms.CharField(max_length=50)

class BaseIssuerCreationForm(ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification.")

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
    class Meta:
        model = Color
        exclude = ('issuer', 'color_id', 'address', 'is_confirmed', 'is_confirming')


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Color, Polis, PolisOwner
from django.contrib.auth.models import User


class ColorModelForm(forms.ModelForm):
    class Meta:
        model = Color

class PolisModelForm(forms.ModelForm):
    class Meta:
        model = Polis

class PolisOwnerCreationForm(forms.Form):
    polis_name = forms.CharField(label='Polis name', max_length=50)
    email = forms.EmailField()
    register_url = forms.URLField(label='Polis register url')
    password1 = forms.CharField(label='Password', 
            widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', 
            widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(PolisOwnerCreationForm, self).__init__(*args, **kwargs)
        self.user = None

    def clean_polis_name(self):
        polis_name = self.cleaned_data.get('polis_name')
        try:
            User.objects.get(username=polis_name)
        except User.DoesNotExist:
            return polis_name

        raise forms.ValidationError('A polis with that polis name already exists.')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2


    def save(self):
        user = User(username=self.cleaned_data['polis_name'],
                    email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.save()
        polis = Polis(name=self.cleaned_data['polis_name'],
                      register_url=self.cleaned_data['register_url'])
        polis.save()
        polis_owner = PolisOwner(user=user, polis=polis)
        polis_owner.save()
        return polis_owner


        

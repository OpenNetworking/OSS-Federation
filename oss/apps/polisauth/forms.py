from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Color, Polis, PolisOwner


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

    def clean(self):
        print 'hi'
        user_data = dict(username=self.cleaned_data['polis_name'],
                    email=self.cleaned_data['email'],
                    password1=self.cleaned_data['password1'],
                    password2=self.cleaned_data['password2'])

        user_form = UserCreationForm(user_data)

        polis_data = dict(name=self.cleaned_data['polis_name'],
                          register_url=self.cleaned_data['register_url'])

        polis_form = PolisModelForm(polis_data)

        if user_form.is_valid() and polis_form.is_valid():
            self.user = user_form.save(commit=False)
            print self.user.username
            self.polis = polis_form.save(commit=False)
            print self.polis.name
        else:
            raise forms.ValidationError('hi')


    def save(self):
        self.user.save()
        self.polis.save()
        polis_owner = PolisOwner(user=self.user, polis=self.polis)
        polis_owner.save()
        return polis_owner


        

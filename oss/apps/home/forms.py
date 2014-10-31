from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm

from oss.apps.polisauth.models import Color

class HomeAuthenticationForm(AdminAuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(HomeAuthenticationForm, self) \
             .__init__(*args, **kwargs)

        self.fields['username'] \
            .widget.attrs['class'] = 'form-control'

        self.fields['username'] \
            .widget.attrs['placeholder'] = 'Username'

        self.fields['password'] \
            .widget.attrs['class'] = 'form-control'

        self.fields['password'] \
            .widget.attrs['placeholder'] = 'Password'
    
    def confirm_login_allowed(self, user):
        if user.is_staff or user.is_superuser:
            raise forms.ValidationError(
                'login fail',
                code='invaild_login'
            )

        if not user.is_active:
            raise forms.ValidationError(
                'login fail',
                code='invaild_login'
            )

class LicenseCreationForm(forms.ModelForm):
    color_name = forms.CharField(label="color name")
    address = forms.CharField(label="address")

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop("user", "")
        try:
            tmp_obj = Color.objects.latest("color_number")
            print tmp_obj.color_number
            self._color_number = tmp_obj.color_number + 1
        except Color.DoesNotExist:
            self._color_number = 1

        super(LicenseCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Color
        fields = ("color_name", "address",)

    def clean_color_name(self):
        color_name = self.cleaned_data['color_name']

        try:
            Color.objects.get(color_name=color_name)
        except Color.DoesNotExist:
            return color_name

        raise forms.ValidationError('duplicate color name', code='duplicate color name')

    def clean_address(self):
        color_addr = self.cleaned_data['address']

        try:
            Color.objects.get(address=color_addr)
        except Color.DoesNotExist:
            return color_addr

        raise forms.ValidationError('duplicate color address', code='duplicate color address')

    def save(self, commit=True):
        color = super(LicenseCreationForm, self).save(commit=False)
        color.polis_id = self._user
        color.color_number = self._color_number
        if commit:
            color.save()
            self.save_m2m()
        return color

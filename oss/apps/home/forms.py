from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm

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



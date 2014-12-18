from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm

class AccountAuthenticationForm(AdminAuthenticationForm):
    """
    Custom login form html attribute
    """
    def __init__(self, *args, **kwargs):
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

    def confirm_login_allowed(self, user):
        pass
        """
        if not user.is_confirmed:
            raise forms.ValidationError(
                'login fail',
                 code='invalid_login'
            )
        """

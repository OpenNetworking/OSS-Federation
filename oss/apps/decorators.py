from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

STAFF_LOGIN_URL = '/adminapp/login/'
NON_STAFF_LOGIN_URL = '/home/login/'

def non_staff_required(function=None,
                       redirect_field_name=REDIRECT_FIELD_NAME,
                       login_url=NON_STAFF_LOGIN_URL):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and not u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)

    return actual_decorator

def staff_required(function=None,
                   redirect_field_name=REDIRECT_FIELD_NAME,
                   login_url=STAFF_LOGIN_URL):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)

    return actual_decorator


from django.shortcuts import render, Http404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.i18n import set_language as django_set_language
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (login as auth_login,
                                       logout as auth_logout)

from baseissuer.views import (BaseIssuerDetailView, BaseIssuerUpdateView,
                              issuer_add_color)
from baseissuer.forms import BaseIssuerCreationForm

from .forms import AccountAuthenticationForm

ACCOUNT_AUTO_CONFIRM = getattr(settings, 'ACCOUNT_AUTO_CONFIRM', False)
ACCOUNT_ADD_COLOR_AUTO_CONFIRM = getattr(settings,
                                     'ACCOUNT_ADD_COLOR_AUTO_CONFIRM',
                                     False)
@require_POST
@csrf_exempt
def set_language(request):
    return django_set_language(request)

def account_signup(request):
    if request.method == "POST":
        form = BaseIssuerCreationForm(request.POST)
        if form.is_valid():
            # send an confirmations email to issuer
            issuer = form.save(commit=True)
            if settings.ACCOUNT_AUTO_CONFIRM == True:
                issuer.is_confirmed = True
                issuer.save()
                return render(request, 'accounts/signup_success.html')
            return render(request, 'accounts/thanks_signup.html')
    else:
        form = BaseIssuerCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def account_login(request):
    return auth_login(request,
               template_name='accounts/login.html',
               authentication_form=AccountAuthenticationForm)

def account_logout(request):
    return auth_logout(request, next_page=reverse('accounts:account_profile'))

@login_required
def home(request):
    """
    Just redirect to profile
    """
    return HttpResponseRedirect(reverse('accounts:account_profile'))

@login_required
def account_profile(request):
    user = request.user
    view = BaseIssuerDetailView.as_view(
               context_object_name='account',
               template_name='accounts/account_profile.html')
    return view(request, pk=user.pk)

@login_required
def account_update(request):
    user = request.user
    view = BaseIssuerUpdateView.as_view(
               template_name='accounts/account_update.html',
               success_url=reverse('accounts:account_profile'))
    return view(request, pk=user.pk)

@login_required
def account_add_color(request):
    return issuer_add_color(request,
               issuer_pk=request.user.pk,
               confirm=ACCOUNT_ADD_COLOR_AUTO_CONFIRM,
               template_name='accounts/account_add_color.html',
               redirect_to=reverse('accounts:account_profile'))


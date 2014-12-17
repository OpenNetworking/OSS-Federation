from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (login as auth_login,
                                       logout as auth_logout)

from baseissuer.views import (BaseIssuerDetailView, BaseIssuerUpdateView,
                               issuer_add_color)

from .forms import AccountAuthenticationForm

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
               template_name='accounts/account_add_color.html',
               redirect_to=reverse('accounts:account_profile'))


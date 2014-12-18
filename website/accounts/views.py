from django.shortcuts import render, Http404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (login as auth_login,
                                       logout as auth_logout)
from django.template import Context
from django.template.loader import get_template
from django.core.mail import send_mail
from django.conf import settings

from baseissuer.views import (BaseIssuerDetailView, BaseIssuerUpdateView,
                              issuer_add_color)
from baseissuer.forms import BaseIssuerCreationForm
from simple_email_confirmation.models import (EmailAddress,
                                              EmailConfirmationExpired)

from .forms import AccountAuthenticationForm

def confirm_signup(request, key):
    """
    Attempt to confirm an email using the given key
    update the baseissuer in DB that was confirmed, or raise an exception.
    """
    try:
        email_address = EmailAddress.objects.get(key=key)
        print email_address
        issuer = email_address.user
        issuer.confirm_email(key)
        issuer.is_confirm = issuer.is_confirmed
        issuer.save()
        return HttpResponse('confirm success')
    except EmailAddress.DoesNotExist as e:
        raise Http404
    except EmailConfirmationExpired as e:
        return HttpResponse('confirmed failed')

def render_mail_template(template_name, host, confirmation_key):
    context = Context({'confirmation_key': confirmation_key,
                       'host': host})
    mail_template = get_template(template_name)
    return mail_template.render(context)

def account_signup(request):
    if request.method == "POST":
        form = BaseIssuerCreationForm(request.POST)
        if form.is_valid():
            # send an confirmations email to issuer
            issuer = form.save(commit=True)
            msg = render_mail_template("accounts/confirmation_mail.txt",
                                        request.get_host(),
                                        issuer.confirmation_key)
            send_mail('[%s] Confirm E-mail Address From Alliance' % 'opennet.org',
                      msg, settings.EMAIL_HOST_USER, [issuer.email], fail_silently=False)
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
               template_name='accounts/account_add_color.html',
               redirect_to=reverse('accounts:account_profile'))


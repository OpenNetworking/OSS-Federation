import os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings

from bitcoinrpc.connection import BitcoinConnection
import logging

import config

from .models import BaseIssuer, Color, Address
from .forms import (BaseIssuerCreationForm, BaseIssuerUpdateForm,
                    ColorCreationForm, AddressInputForm)

from simple_email_confirmation.models import (EmailAddress, EmailConfirmationExpired)


logger = logging.getLogger(__name__)

def confirm_email(request, key):
    """
    Attempt to confirm an email using the given key
    update the baseissuer in DB that was confirmed, or raise an exception.
    """
    try:
        print key
        issuer = EmailAddress.objects.get(key=key).user
        issuer.confirm_email(key)
        issuer.is_confirm = issuer.is_confirmed
        issuer.save()
        return HttpResponse('sussceed')
    except EmailConfirmationExpired as e:
        return HttpResponse('confirmed failed')

def issuer_create(request, template_name='issuer/form.html',
                  redirect_to=None,
                  confirm=False):
    if request.method == "POST":
        issuer_form = BaseIssuerCreationForm(request.POST)

        if issuer_form.is_valid():
            # send an confirmations email to issuer
            text_path = os.path.realpath(os.path.dirname(__file__))
            fp = open(text_path + '/textfile', 'rb')
            msg = fp.read()
            fp.close()
            issuer = issuer_form.save(commit=True)
            msg = msg % issuer.confirmation_key
            send_mail('[%s] Confirm E-mail Address From Alliance' % 'opennet.org',
                      msg, settings.EMAIL_HOST_USER, [issuer.email], fail_silently=False)

            if redirect_to:
                return HttpResponseRedirect(redirect_to)

            return HttpResponse('success')
    else:
        issuer_form = BaseIssuerCreationForm()

    return render(request, template_name,
                  {'issuer_form': issuer_form})

@require_http_methods(['POST'],)
def issuer_delete(request, pk):
    try:
        issuer = BaseIssuer.objects.get(pk=pk)
    except BaseIssuer.DoesNotExist:
        raise Http404
    issuer.delete()
    if request.is_ajax():
        return HttpResponse()
    return HttpResponse('delete success')

@require_http_methods(['POST'],)
def issuer_accept(request, pk):
    issuer = get_object_or_404(BaseIssuer, pk=pk)
    issuer.active()
    return HttpResponse('issuer accept success')

def issuer_add_color(request, issuer_pk, confirm=False,
                     template_name="issuer/issuer_add_color.html",
                     redirect_to=None):
    issuer = get_object_or_404(BaseIssuer, pk=issuer_pk)
    if request.method == 'POST':
        color_form = ColorCreationForm(request.POST)
        address_form = AddressInputForm(request.POST)
        if color_form.is_valid() and address_form.is_valid():
            #create address
            raw_address = address_form.cleaned_data.get('address')
            address = Address(address=raw_address)
            address.save()

            color = color_form.save(commit=False)
            color.address = address
            color.issuer = issuer
            last_color = (Color.objects.all()
                                       .order_by('color_id').last())

            color_id = 1
            if last_color:
                color_id = last_color.color_id + 1
            color.color_id = color_id
            if confirm:
                color.is_confirmed = True
            color.save()

            if not redirect_to:
                redirect_to = '/issuer/{0}/detail/'.format(issuer_pk)

            return HttpResponseRedirect(redirect_to)
    else:
        color_form = ColorCreationForm()
        address_form = AddressInputForm()

    return render(request, template_name,
                  {'color_form': color_form, 'address_form': address_form,
                   'issuer': issuer })

@require_http_methods(['POST',])
def color_reject(request, pk):
    color = get_object_or_404(Color, pk=pk)
    color.delete()
    return HttpResponse('reject success')

@require_http_methods(['POST',])
def color_accept(request, pk):
    color = get_object_or_404(Color, pk=pk)

    try:
        rpc = BitcoinConnection(config.RPC_AE_USER,
                                config.RPC_AE_PASSWORD,
                                config.RPC_AE_HOST,
                                config.RPC_AE_PORT)
        ret = rpc.sendlicensetoaddress(color.address.address, color.color_id)
    except Exception as e:
        logger.error(str(e))
        return HttpResponse('failed to send license to Aliance')

    color.is_confirmed = True
    color.save()
    return HttpResponse('accept success')

class BaseIssuerUpdateView(UpdateView):

    model = BaseIssuer
    fields = ['name', 'url']
    template_name_suffix = '_update'

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        else:
            obj = self.get_object()
            return '/issuer/{0}/detail/'.format(obj.pk)

class BaseIssuerDetailView(DetailView):

    model = BaseIssuer

class BaseIssuerListView(ListView):

    #queryset = BaseIssuer.objects.filter(is_confirmed=True)
    queryset = BaseIssuer.objects.all()
    context_object_name = 'issuer_list'

    def get_queryset(self):
        queryset = super(BaseIssuerListView, self).get_queryset()
        search = self.request.GET.get('search', None)
        if search is not None:
            queryset = queryset.filter(Q(user__username__icontains=search)|
                                       Q(address__address__icontains=search)|
                                       Q(register_url__icontains=search))
        queryset = queryset.distinct()
        return queryset

class UnconfirmedBaseIssuerListView(ListView):

    #queryset = BaseIssuer.objects.filter(is_confirmed=False)
    queryset = BaseIssuer.objects.all()
    context_object_name = 'issuer_list'

    def get_queryset(self):
        queryset = super(UnconfirmedBaseIssuerListView, self).get_queryset()
        search = self.request.GET.get('search', None)
        if search is not None:
            queryset = queryset.filter(Q(user__username__icontains=search)|
                                       Q(address__address__icontains=search)|
                                       Q(register_url__icontains=search))
        queryset = queryset.distinct()
        return queryset

class ColorListView(ListView):

    queryset = Color.objects.filter(is_confirmed=True)
    context_object_name = 'color_list'

class UnconfirmedColorListView(ListView):

    queryset = Color.objects.filter(is_confirmed=False)
    context_object_name = 'color_list'
    template_name = 'issuer/unconfirmed_color_list.html'

class ColorDetailView(DetailView):

    model = Color


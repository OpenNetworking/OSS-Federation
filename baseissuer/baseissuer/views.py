from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.db.models import Q
from bitcoinrpc.connection import BitcoinConnection
import logging

import config

from .models import BaseIssuer, Color, Address
from .forms import (BaseIssuerCreationForm, BaseIssuerUpdateForm,
                    ColorCreationForm, AddressInputForm)

logger = logging.getLogger(__name__)

def issuer_create(request, template_name='issuer/form.html',
                  redirect_to=None,
                  confirm=False):
    if request.method == "POST":
        issuer_form = BaseIssuerCreationForm(request.POST)
        issuer = None

        if issuer_form.is_valid():
            issuer = issuer_form.save(commit=True)
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
                messages.success(request,
                                 'add color success')
                color.is_confirmed = True
            else:
                messages.info(request,
                              'waiting for approve')

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


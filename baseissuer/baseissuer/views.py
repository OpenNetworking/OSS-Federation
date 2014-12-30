import os
import urllib
import urllib2
import json
import collections
from threading import Thread
from time import sleep

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.db.models import Q
from django.conf import settings

from bitcoinrpc import connect_to_local
import logging

from api_query.api_query import APIClient
from .models import BaseIssuer, Color, Address
from .forms import (BaseIssuerCreationForm, BaseIssuerUpdateForm,
                    ColorCreationForm, AddressInputForm)

logger = logging.getLogger(__name__)

def issuer_create(request, template_name='issuer/form.html',
                  redirect_to=None,
                  confirm=False):
    if request.method == "POST":
        issuer_form = BaseIssuerCreationForm(request.POST)

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
    issuer.confirm()
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

    thread = Thread(target=send_license_req_to_alliance, args=(color,))
    thread.start()

    color.is_confirming = True
    color.save()

    return HttpResponse('confirming')

def send_license_req_to_alliance(color):

    try:
        rpc = connect_to_local()

        rpc.mint(1, 0)

        while True:
            ret_balance = rpc.getbalance()

            if '0' in ret_balance and ret_balance['0'] >= 1:
                break
            sleep(5)

        rpc.sendlicensetoaddress(color.address.address, color.color_id)

        color.is_confirming = False
        color.is_confirmed = True
        color.save()

    except Exception as e:
        logger.error(str(e))
        color.is_confirming = False
        color.is_confirmed = False
        color.save()

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

    queryset = BaseIssuer.objects.filter(is_confirmed=True)
    context_object_name = 'issuer_list'

    def get_queryset(self):
        queryset = super(BaseIssuerListView, self).get_queryset()
        search = self.request.GET.get('search', None)
        if search is not None:
            queryset = queryset.filter(Q(user__username__icontains=search)|
                                       Q(address__address__icontains=search)|
                                       Q(register_url__icontains=search))
        queryset = queryset.distinct()

        for issuer in queryset:
            # get balance
            balance_list = []
            color_addr_array = []

            colors = Color.objects.filter(issuer__name=issuer.name)

            if colors.count() <= 0:
                issuer.balance_list = []
                issuer.tx_count = 0
            else:
                api_client = APIClient()
                try:
                    for color in colors:
                        color_addr_array.append(color.address.address)

                    ret = api_client.get_issuer_balance(color_addr_array)

                except Exception as e:
                    err_msg = '%s(%s)' % ('failed to get balance from issuer list', str(e))
                    logger.error(err_msg)
                    return queryset

                if api_client.success:
                    all_balance = ret['data']
                else:
                    err_msg = '%s(%s)' % ('failed to get balance from issuer list', api_client.err_msg)
                    logger.error(err_msg)
                    return queryset

                for k, v in all_balance.items():
                    tmp_balance = collections.OrderedDict([('color', int(k)), ('amount', float(v))])
                    balance_list.append(tmp_balance)

                issuer.balance_list = balance_list

                # get tx count
                tx_colors_array = []

                for color in colors:
                    tx_colors_array.append(color.color_id)

                api_client = APIClient()
                try:
                    ret = api_client.get_txs_list(colors=tx_colors_array)
                except Exception as e:
                    err_msg = '%s(%s)' % ('failed to get txs listt from issuer list', str(e))
                    logger.error(err_msg)
                    return queryset

                if api_client.success:
                    issuer.tx_count = ret['data']['total_count']
                else:
                    err_msg = '%s(%s)' % ('failed to get txs count from issuer list', api_client.err_msg)
                    logger.error(err_msg)
                    issuer.tx_count = 0

        return queryset

class UnconfirmedBaseIssuerListView(ListView):

    queryset = BaseIssuer.objects.filter(is_confirmed=False)
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


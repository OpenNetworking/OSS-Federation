import urllib2
import json
import math
import os
import collections

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin.forms import AdminAuthenticationForm
from django.utils.decorators import method_decorator
import logging

from baseissuer.models import BaseIssuer as Issuer, Color
from baseissuer.views import (BaseIssuerDetailView, issuer_create,
                              BaseIssuerListView, issuer_delete,
                              issuer_accept,
                              color_reject, color_accept,
                              BaseIssuerUpdateView,
                              UnconfirmedBaseIssuerListView,
                              issuer_add_color, ColorListView,
                              UnconfirmedColorListView, ColorDetailView)

from alliance.views import alliance_list
from utils.decorators import staff_required
from utils.oss_http_response import JsonOkResp, JsonErrResp

import config

logger = logging.getLogger(__name__)

@staff_required
def index(request):
    return render(request, 'adminapp/index.html')

@staff_required
def admin_issuer_create(request):
    return issuer_create(request,
                         template_name='adminapp/issuer_create.html',
                         redirect_to='/adminapp/issuer_list/',
                         confirm=config.AUTO_CONFIRM_ISSUER_REGISTRATION)

@staff_required
def admin_issuer_add_color(request, pk):
    redirect_to = '/adminapp/issuer_detail/{0}/'.format(pk)
    return issuer_add_color(request, pk,
                            template_name='adminapp/issuer_add_color.html',
                            redirect_to=redirect_to,
                            confirm=config.AUTO_CONFIRM_COLOR_REGISTRATION)

@staff_required
def admin_issuer_delete(request, pk):
    return issuer_delete(request, pk)

@staff_required
def admin_issuer_accept(request, pk):
    return issuer_accept(request, pk)

@staff_required
def admin_color_reject(request, pk):
    return color_reject(request, pk)

@staff_required
def admin_color_accept(request, pk):
    return color_accept(request, pk)

class AdminIssuerDetailView(BaseIssuerDetailView):

    template_name = 'adminapp/issuer_detail.html'
    context_object_name = 'issuer'

    @method_decorator(staff_required)
    def dispath(request, *args, **kwargs):
        return super(AdminIssuerDetailView,
                     self).dispatch(request, *args, **kwargs)

class AdminIssuerUpdateView(BaseIssuerUpdateView):

    template_name = 'adminapp/issuer_update.html'
    context_object_name = 'issuer'

    def get_success_url(self):
        return '/adminapp/issuer_list/'

    @method_decorator(staff_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminIssuerUpdateView,
                     self).dispatch(request, *args, **kwargs)

class AdminIssuerListView(BaseIssuerListView):

    template_name = 'adminapp/issuer_list.html'

    @method_decorator(staff_required)
    def dispath(request, *args, **kwargs):
        return super(AdminIssuerListView,
                     self).dispatch(request, *args, **kwargs)

class AdminUnconfirmedIssuerListView(UnconfirmedBaseIssuerListView):

    template_name = 'adminapp/unconfirmed_issuer_list.html'

    @method_decorator(staff_required)
    def dispath(request, *args, **kwargs):
        return super(AdminUnconfirmedIssuerListView,
                     self).dispatch(request, *args, **kwargs)

class AdminColorListView(ColorListView):

    template_name = 'adminapp/color_list.html'

    @method_decorator(staff_required)
    def dispath(request, *args, **kwargs):
        return super(AdminUnconfirmedBaseIssuerListView,
                     self).dispatch(request, *args, **kwargs)

class AdminUnconfirmedColorListView(UnconfirmedColorListView):

    template_name = 'adminapp/unconfirmed_color_list.html'

    @method_decorator(staff_required)
    def dispath(request, *args, **kwargs):
        return super(AdminUnconfirmedIssuerListView,
                     self).dispatch(request, *args, **kwargs)

class AdminColorDetailView(ColorDetailView):

    template_name = 'adminapp/color_detail.html'

    @method_decorator(staff_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminColorDetailView,
                     self).dispatch(request, *args, **kwargs)

@staff_required
def txs_list(request):
    """
    Get blockchain transaction list.

    Blockchain OSS can list all transactions
    All transactions can be filtered by color & issuer
    """
    tx_colors_str = ""
    tx_addrs_str = ""

    tx_addrs_array = []

    tx_addrs_str_array = []

    tx_colors = request.GET.getlist('color')
    tx_issuers_id = request.GET.getlist('issuer')
    tx_start = request.GET.get('start', 1)
    tx_end = request.GET.get('end', 20)

    tx_mode = 0

    if len(tx_colors) > 0:
        tx_colors_array = ['%s=%s' % ('color', color) for color in tx_colors]
        tx_colors_str = '&'.join(tx_colors_array)

    tx_start_str = '%s=%s' % ('start', tx_start)
    tx_end_str = '%s=%s' % ('end', tx_end)

    # get all color address related to issuer
    for cur_issuer_id in tx_issuers_id:
        colors = Color.objects.all().filter(issuer__pk=cur_issuer_id)
        for color in colors:
            # cur color address
            tx_addrs_array.append(color.address)
            # history color address

    tx_addrs_str_array = ['%s=%s' % ('addr', addr.address) for addr in tx_addrs_array]
    tx_addrs_str = '&'.join(tx_addrs_str_array)

    url = '%s%s%s&' % (config.API_HOST, 'tx/?mode=', str(tx_mode))
    # remote api call to get txs_list
    if tx_addrs_str:
        url = '%s%s&' % (url, tx_addrs_str)
    if tx_colors_str:
        url = '%s%s&' % (url, tx_colors_str)
    if tx_start_str:
        url = '%s%s&' % (url, tx_start_str)
    if tx_end_str:
        url = '%s%s&' % (url, tx_end_str)

    try:
        ret_jdata = json.load(urllib2.urlopen(url))['data']
    except Exception as e:
        logger.error(str(e))
        return HttpResponse(str(e))

    page_count = int(math.ceil(ret_jdata['total_count'] / (int(tx_end) - int(tx_start) + 1)))
    cur_page = int(math.ceil(int(tx_end) / (int(tx_end) - int(tx_start) + 1)))

    issuers = Issuer.objects.all()

    return render(request, 'adminapp/txs_list.html', dict(txs=ret_jdata['transaction'],
                                                          page_count=page_count,
                                                          cur_page=cur_page,
                                                          colors=ret_jdata['colors'],
                                                          cur_colors=tx_colors,
                                                          issuers=issuers,
                                                          cur_issuers=tx_issuers_id))

@staff_required
def tx(request, tx_id=None):
    if request.is_ajax():
        if tx_id is None:
            return JsonErrResp(500, 'failed to get specific tx information (empty tx id)')

        url = '%s%s%s' % (config.API_HOST, 'transactions?hash=', tx_id)
        try:
            return JsonOkResp(json.load(urllib2.urlopen(url)))
        except Exception as e:
            err_msg = '%s (%s)' % ('failed to get specific tx information', str(e))
            return JsonErrResp(500, err_msg)
    else:
        return render(request, 'adminapp/')

@staff_required
def admin_alliance_list(request):
    print "admin_aalice"
    return alliance_list(request)


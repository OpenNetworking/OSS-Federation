import urllib
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
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.i18n import set_language as django_set_language
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
from utils.decorators import staff_required, ajax_staff_required
from utils.oss_http_response import JsonOkResp, JsonErrResp, HttpErrResp
from api_query.api_query import APIClient

import config

logger = logging.getLogger(__name__)

@require_POST
@csrf_exempt
def set_language(request):
    return django_set_language(request)

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
@ajax_staff_required
def admin_issuer_delete(request, pk):
    return issuer_delete(request, pk)

@ajax_staff_required
def admin_issuer_accept(request, pk):
    return issuer_accept(request, pk)

@ajax_staff_required
def admin_color_reject(request, pk):
    return color_reject(request, pk)

@ajax_staff_required
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

    query_data = {}
    query_string = ''

    tx_issuers_addrs = []

    tx_colors = request.GET.getlist('color')
    tx_issuers_id = request.GET.getlist('issuer')
    tx_date_from = request.GET.get('from', None)
    tx_date_to = request.GET.get('to', None)
    tx_start = request.GET.get('start', 1)
    tx_end = request.GET.get('end', 20)

    # get all color address related to issuer
    for cur_issuer_id in tx_issuers_id:
        colors = Color.objects.all().filter(issuer__pk=cur_issuer_id)
        for color in colors:
            tx_issuers_addrs.append(color.address)

    api_client = APIClient()

    try:
        ret = api_client.get_txs_list(colors=tx_colors,
                                      issuer_addrs=tx_issuers_addrs,
                                      date_from=tx_date_from,
                                      date_to=tx_date_to,
                                      start=tx_start,
                                      end=tx_end)
    except Exception as e:
        logger.error(str(e))
        return HttpErrResp(api_client.code, str(e))

    if api_client.success:
        ret_jdata = ret['data']
    else:
        err_msg = '%s(%s)' % ('failed to get transaction list', api_client.err_msg)
        logger.error(err_msg)
        return HttpErrResp(api_client.code, err_msg)

    page_count = int(math.ceil(ret_jdata['total_count'] / (int(tx_end) - int(tx_start) + 1)))
    cur_page = int(math.ceil(int(tx_end) / (int(tx_end) - int(tx_start) + 1)))

    issuers = Issuer.objects.all()

    return render(request, 'adminapp/txs_list.html', dict(txs=ret_jdata['transaction'],
                                                          page_count=page_count,
                                                          cur_page=cur_page,
                                                          colors=ret_jdata['colors'],
                                                          cur_colors=tx_colors,
                                                          issuers=issuers,
                                                          cur_issuers=tx_issuers_id,
                                                          cur_date_from=tx_date_from,
                                                          cur_date_to=tx_date_to))

@staff_required
def tx(request, tx_id=None):
    if request.is_ajax():
        if tx_id is None:
            return JsonErrResp(500,
                               'tx id is empty when get transaction info.')

        api_client = APIClient()

        try:
            ret = api_client.get_tx_info(tx_id)
        except Exception as e:
            err_msg = ('%s (%s)' %
                       ('failed to get specific tx information due to exception', str(e)))
            logger.error(err_msg)
            return JsonErrResp(api_client.code, err_msg)

        if api_client.success:
            return JsonOkResp(ret)
        else:
            err_msg = ('%s (%s)' %
                       ('failed to get specific tx information', api_client.err_msg))
            logger.error(err_msg)
            return JsonErrResp(api_client.code, err_msg)
    else:
        return render(request, 'adminapp/')

@staff_required
def admin_alliance_list(request):
    return alliance_list(request)


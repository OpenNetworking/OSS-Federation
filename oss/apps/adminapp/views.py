import urllib2
import json
import math
import os
import collections

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin.forms import AdminAuthenticationForm
#from bitcoinrpc.connection import BitcoinConnection
from django.utils.decorators import method_decorator

from oss.apps.issuer.models import Issuer, Color
from oss.apps.issuer.views import (IssuerDetailView, issuer_create,
                                   IssuerListView, issuer_delete,
                                   UnconfirmedIssuerListView,
                                   issuer_add_color, ColorListView,
                                   UnconfirmedColorListView)
from oss.apps.decorators import staff_required

import config

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

class AdminIssuerDetailView(IssuerDetailView):

    template_name = 'adminapp/issuer_detail.html'

    @method_decorator(staff_required)
    def dispath(request, *args, **kwargs):
        return super(AdminIssuerDetailView,
                     self).dispatch(request, *args, **kwargs)

class AdminIssuerListView(IssuerListView):

    template_name = 'adminapp/issuer_list.html'

    @method_decorator(staff_required)
    def dispath(request, *args, **kwargs):
        return super(AdminIssuerListView,
                     self).dispatch(request, *args, **kwargs)

class AdminUnconfirmedIssuerListView(UnconfirmedIssuerListView):

    template_name = 'adminapp/unconfirmed_issuer_list.html'

    @method_decorator(staff_required)
    def dispath(request, *args, **kwargs):
        return super(AdminUnconfirmedIssuerListView,
                     self).dispatch(request, *args, **kwargs)

class AdminColorListView(ColorListView):

    template_name = 'adminapp/color_list.html'

    @method_decorator(staff_required)
    def dispath(request, *args, **kwargs):
        return super(AdminUnconfirmedIssuerListView,
                     self).dispatch(request, *args, **kwargs)

class AdminUnconfirmedColorListView(UnconfirmedColorListView):

    template_name = 'adminapp/unconfirmed_color_list.html'

    @method_decorator(staff_required)
    def dispath(request, *args, **kwargs):
        return super(AdminUnconfirmedIssuerListView,
                     self).dispatch(request, *args, **kwargs)



@staff_required
def txs_list(request):
    """ get blockchain transaction list

    Blockchain OSS can list all transactions
    All transactions can be filtered by color & issuer
    """
    tx_colors_str = ""

    tx_colors = request.GET.getlist("color")
    tx_addrs = request.GET.getlist("issuer")
    tx_start = request.GET.get("start", 1)
    tx_end = request.GET.get("end", 20)

    if len(tx_colors) != 0:
        tx_colors_array = ["%s=%s" % ("color", color) for color in tx_colors]
        tx_colors_str = '&'.join(tx_colors_array)

    tx_start_str = "%s=%s" % ("start", tx_start)
    tx_end_str = "%s=%s" % ("end", tx_end)

    # remote api call to get txs_list
    parser = _config_get()
    base_url = parser.get("api", "host")
    url = "%s%s?%s&%s&%s" % (base_url, "tx/", tx_start_str, tx_end_str, tx_colors_str)

    try:
        ret_jdata = json.load(urllib2.urlopen(url))["data"]
    except urllib2.HTTPError as e:
        # TODO: log error
        print e.reason
        pass

    page_count = int(math.ceil(ret_jdata["total_count"] / (int(tx_end) - int(tx_start) + 1)))
    cur_page = int(math.ceil(int(tx_end) / (int(tx_end) - int(tx_start) + 1)))

    return render(request, "adminapp/txs_list.html", dict(txs=ret_jdata["transaction"],
                                                          page_count=page_count,
                                                          cur_page=cur_page,
                                                          colors=ret_jdata["colors"],
                                                          cur_colors=tx_colors))

import urllib2
import json
import math
import os
import collections

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.admin.forms import AdminAuthenticationForm
from bitcoinrpc.connection import BitcoinConnection

from oss.apps.polisauth.models import PolisOwner, Color
from oss.apps.polisauth.forms import PolisOwnerCreationForm
from oss.apps.adminapp.config import _config_get
from .decorators import staff_required


ADMINAPP_LOGIN_URL = '/adminapp/login'

# Create your views here.

@staff_required(login_url=ADMINAPP_LOGIN_URL)
def index(request):
    return render(request, 'adminapp/index.html')

@staff_required(login_url=ADMINAPP_LOGIN_URL)
def polis_list(request):
    poleis = [polis for polis in PolisOwner.objects.all() if polis.is_active()]
    return render(request, 'adminapp/polis_list.html', 
                  dict(poleis=poleis))

@staff_required(login_url=ADMINAPP_LOGIN_URL)
def new_polis_list(request):
    poleis = [polis for polis in PolisOwner.objects.all() 
              if not polis.is_active()]
    return render(request, 'adminapp/new_polis_list.html', 
                  dict(poleis=poleis))


@staff_required(login_url=ADMINAPP_LOGIN_URL)
@require_http_methods(['POST',])
def polis_owner_confirm(request, pk):
    try:
        polis_owner = PolisOwner.objects.get(pk=pk)
    except PolisOwner.DoseNotExist:
        raise Http404
    polis_owner.user.is_active = True
    polis_owner.user.save()
    if request.is_ajax():
        return HttpResponse()
    return HttpResponse()

@staff_required(login_url=ADMINAPP_LOGIN_URL)
def polis_owner_create(request):
    form = PolisOwnerCreationForm()
    if request.method == "POST":
        form = PolisOwnerCreationForm(request.POST)
        if form.is_valid():
            polis_owner = form.save()
            polis_owner.active()
            return HttpResponseRedirect(reverse('adminapp:polis_list'))

    return render(request, 'adminapp/polis_owner_create.html', dict(form=form))

@staff_required(login_url=ADMINAPP_LOGIN_URL)
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

@staff_required(login_url=ADMINAPP_LOGIN_URL)
def license_request_list(request):
    unconfirmed_colors = Color.objects.all().filter(is_license=False)

    return render(request, "adminapp/license_request_list.html", dict(unconfirmed_colors=unconfirmed_colors))

@staff_required(login_url=ADMINAPP_LOGIN_URL)
def send_license_to_address(request):
    # bitcoin rpc
    if request.is_ajax():
    # sendlicensetoaddress
    parser = _config_get()

    if request.is_ajax():

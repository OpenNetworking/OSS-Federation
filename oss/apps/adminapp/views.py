from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.admin.forms import AdminAuthenticationForm
from oss.apps.polisauth.models import PolisOwner
from oss.apps.polisauth.forms import PolisOwnerCreationForm
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

            
    


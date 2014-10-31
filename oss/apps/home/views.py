from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test

from oss.apps.polisauth.models import Color
from oss.apps.polisauth.forms import PolisOwnerCreationForm
from oss.apps.home.forms import LicenseCreationForm
from .decorators import non_staff_required

# Create your views here.

HOME_LOGIN_URL = '/home/login/'

@non_staff_required(login_url=HOME_LOGIN_URL)
def index(request):
    return render(request, 'home/index.html')


def signup(request):
    form = PolisOwnerCreationForm()
    if request.method == "POST":
        form = PolisOwnerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('wating for accept')

    return render(request, 'home/signup.html', dict(form=form))

def license_detail(request, color_number):
    color = get_object_or_404(Color, pk=color_number)
    return render(request, 'home/license_detail.html', dict(color=color))
    
@non_staff_required(login_url=HOME_LOGIN_URL)
def license_list(request):
    colors = Color.objects.all()
    return render(request, "home/license_list.html", dict(colors=colors))

@non_staff_required(login_url=HOME_LOGIN_URL)
def create_license(request):
    """ create a new license or list license"""
    if request.method == "POST":
        # create a new license
        form = LicenseCreationForm(request.POST, user=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home:license_list'))
    else:
        # list license
        form = LicenseCreationForm()

    return render(request, 'home/create_license.html', dict(form=form))

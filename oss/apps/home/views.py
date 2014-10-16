from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from oss.apps.polisauth.forms import PolisOwnerCreationForm
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




from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from oss.apps.issuer.views import issuer_create
from oss.apps.decorators import non_staff_required

# Create your views here.


@non_staff_required
def index(request):
    return render(request, 'home/index.html')


def signup(request, *args, **kwargs):
    return issuer_create(request, *args, **kwargs)




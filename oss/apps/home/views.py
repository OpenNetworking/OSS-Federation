from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required




# Create your views here.

@login_required
def index(request):
    return render(request, 'home/index.html')

def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home:index'))




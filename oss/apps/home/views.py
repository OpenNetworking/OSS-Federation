from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from oss.apps.polisauth.forms import PolisOwnerCreationForm

# Create your views here.

@login_required
def index(request):
    return render(request, 'home/index.html')


def signup(request):
    form = PolisOwnerCreationForm()
    if request.method == "POST":
        form = PolisOwnerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Wait for accept')

    return render(request, 'home/signup.html', dict(form=form))

def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home:index'))




from django.shortcuts import render
from django.http import HttpResponse
from oss.apps.polisauth.forms import PolisOwnerCreationForm

# Create your views here.

def index(request):
    form = PolisOwnerCreationForm()
    if request.method == "POST":
        form = PolisOwnerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('success')

    return render(request, 'adminapp/index.html', dict(form=form))

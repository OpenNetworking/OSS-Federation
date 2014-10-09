from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from oss.apps.polisauth.models import Polis

# Create your views here.

def polis(request):
    polis = Polis.objects.all()
    data = [dict(name=p.name, register_url=p.register_url) for p in polis]
    return JsonResponse(dict(data=data))

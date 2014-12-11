from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from oss.apps.issuer import Issuer, Color

# Create your views here.

def polis_to_dict(polis):
    polis_dict = dict()
    polis_dict['name'] = polis.name
    polis_dict['register_url'] = polis.register_url
    polis_dict['colors'] = [dict(color_number=color.color_number)
                            for color in polis.color_set.all()]
    return polis_dict



def polis_api(request):
    polis = Polis.objects.all()
    data = [dict(name=p.name, register_url=p.register_url) for p in polis]
    data = [polis_to_dict(p) for p in polis]
    return JsonResponse(dict(data=data))


def colors_api(request):
    colors = Color.objects.all()
    data = [dict(color_number=c.color_number,
                 polis_name=c.polis.name) for c in colors]

    return JsonResponse(dict(data=data))

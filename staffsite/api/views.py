from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from baseissuer.models import BaseIssuer, Color

# Create your views here.

def issuer_to_dict(issuer):
    issuer_dict = dict()
    issuer_dict['name'] = issuer.name
    issuer_dict['email'] = issuer.email
    issuer_dict['register_url'] = issuer.url
    issuer_dict['colors'] = [color_to_dict(color)
                             for color in issuer.color_set.all()]
    return issuer_dict

def color_to_dict(color):
    return dict(color_id=color.color_id,
                color_name=color.color_name,
                issuer_name=color.issuer.name)

def issuers_api(request):
    issuers = BaseIssuer.objects.all()
    data = [issuer_to_dict(issuer) for issuer in issuers]
    return JsonResponse(dict(data=data))

def colors_api(request):
    colors = Color.objects.all()
    data = [color_to_dict(color) for color in colors]
    return JsonResponse(dict(data=data))

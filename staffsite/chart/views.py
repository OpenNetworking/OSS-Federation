import json

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from baseissuer.models import BaseIssuer, Color
from utils.statistics_api_client import StatisticsAPIClient

CHART_API_URL = getattr(settings, "CHART_API_URL", "")

def daily_tx_chart(request):
    return render(request, 'chart/daily_tx_chart.html',
                  {"chart_api_url": CHART_API_URL})

def monthly_tx_chart(request):
    return render(request, 'chart/monthly_tx_chart.html',
                  {"chart_api_url": CHART_API_URL})

def yearly_tx_chart(request):
    return render(request, 'chart/yearly_tx_chart.html',
                  {"chart_api_url": CHART_API_URL})

def network_status_chart(request):
    return render(request, 'chart/network_status.html',
                  {"chart_api_url": CHART_API_URL})

def transaction_chart(request):
    return render(request, 'chart/transaction_chart.html',
                  {'chart_api_url': CHART_API_URL,
                   'issuers': BaseIssuer.objects.all(),
                   'colors': Color.objects.all()})

def blockchain_status(request):
    return render(request, 'chart/blockchain_status.html',
                  {'chart_api_url': CHART_API_URL})

def day(request):
    data = [
            {'hour': 1, 'issuer': 'issuer1', 'color': '1', 'total_out':  100, 'tx_num': 2},
            {'hour': 9, 'issuer': 'issuer1', 'color': '2', 'total_out':  10, 'tx_num': 12},
            {'hour': 2, 'issuer': 'issuer3', 'color': '1', 'total_out':  31, 'tx_num': 2},
            {'hour': 10, 'issuer': 'issuer1', 'color': '1', 'total_out':  20, 'tx_num': 2},
            {'hour': 9, 'issuer': 'issuer2', 'color': '3', 'total_out':  77, 'tx_num': 7},
            {'hour': 12, 'issuer': 'issuer1', 'color': '1', 'total_out':  100, 'tx_num': 2},
            {'hour': 3, 'issuer': 'issuer1', 'color': '1', 'total_out':  10, 'tx_num': 2},
            {'hour': 11, 'issuer': 'issuer3', 'color': '4', 'total_out':  30, 'tx_num': 9},
            {'hour': 3, 'issuer': 'issuer1', 'color': '1', 'total_out':  50, 'tx_num': 2},
            {'hour': 18, 'issuer': 'issuer1', 'color': '4', 'total_out':  33, 'tx_num': 10},
            {'hour': 20, 'issuer': 'issuer1', 'color': '1', 'total_out':  13, 'tx_num': 2},
    ]
    return JsonResponse(dict(data=data))

def fakedata(request):
    data = [
            {   'miner': 'm1',
                'color': 1,
                'hour': 10,
                'total_out': 10,
                'tx_num': 30
            },
            {   'miner': 'm2',
                'color': 3,
                'hour': 9,
                'total_out': 120,
                'tx_num': 330
            },
    ]
    return JsonResponse(dict(data=data))

def fakeyear(request):
    data = [
            {   'miner': 'm1',
                'color': 1,
                'month': 10,
                'total_out': 10,
                'tx_num': 30
            },
            {   'miner': 'm2',
                'color': 3,
                'month': 9,
                'total_out': 120,
                'tx_num': 330
            },
            {   'miner': 'm2',
                'color': 3,
                'month': 10,
                'total_out': 120,
                'tx_num': 330
            },
            {   'miner': 'm2',
                'color': 3,
                'month': 1,
                'total_out': 120,
                'tx_num': 330
            },
    ]
    return JsonResponse(dict(data=data))

def fakemonth(request):
    data = [
            {   'miner': 'm1',
                'color': 1,
                'day': 10,
                'total_out': 10,
                'tx_num': 30
            },
            {   'miner': 'm2',
                'color': 3,
                'day': 9,
                'total_out': 120,
                'tx_num': 330
            },
            {   'miner': 'm2',
                'color': 3,
                'day': 10,
                'total_out': 120,
                'tx_num': 330
            },
            {   'miner': 'm2',
                'color': 3,
                'day': 1,
                'total_out': 120,
                'tx_num': 330
            },
    ]
    return JsonResponse(dict(data=data))



def fakedata(request):
    data = [
            {   'miner': 'm1',
                'color': 1,
                'hour': 10,
                'total_out': 10,
                'tx_num': 30
            },
            {   'miner': 'm2',
                'color': 3,
                'hour': 9,
                'total_out': 120,
                'tx_num': 330
            },
    ]
    return JsonResponse(dict(data=data))

def fakeyear(request):
    data = [
            {   'miner': 'm1',
                'color': 1,
                'month': 10,
                'total_out': 10,
                'tx_num': 30
            },
            {   'miner': 'm2',
                'color': 3,
                'month': 9,
                'total_out': 120,
                'tx_num': 330
            },
            {   'miner': 'm2',
                'color': 3,
                'month': 10,
                'total_out': 120,
                'tx_num': 330
            },
            {   'miner': 'm2',
                'color': 3,
                'month': 1,
                'total_out': 120,
                'tx_num': 330
            },
    ]
    return JsonResponse(dict(data=data))

def fakemonth(request):
    data = [
            {   'miner': 'm1',
                'color': 1,
                'day': 10,
                'total_out': 10,
                'tx_num': 30
            },
            {   'miner': 'm2',
                'color': 3,
                'day': 9,
                'total_out': 120,
                'tx_num': 330
            },
            {   'miner': 'm2',
                'color': 3,
                'day': 10,
                'total_out': 120,
                'tx_num': 330
            },
            {   'miner': 'm2',
                'color': 3,
                'day': 1,
                'total_out': 120,
                'tx_num': 330
            },
    ]
    return JsonResponse(dict(data=data))

def qqq(request):
    data = [{}]
    if request.is_ajax():
        return JsonResponse(dict(data=data))
    return render(request, "chart/cors.html")

@login_required
def eee(request):
    print request.user
    data = [{}]
    if request.is_ajax():
        return JsonResponse(dict(data=data))
    return render(request, "chart/cors.html")

@login_required
def api_aeinfo(request):
    client = StatisticsAPIClient()
    res = client.get_aeinfo()
    res_json= res.json()
    res.close()
    return JsonResponse(res_json)


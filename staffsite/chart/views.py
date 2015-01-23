import json

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

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


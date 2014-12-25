import json

from django.shortcuts import render
from django.http import JsonResponse

def daily_tx_chart(request):
    return render(request, 'chart/daily_tx_chart.html')

def monthly_tx_chart(request):
    return render(request, 'chart/monthly_tx_chart.html')

def yearly_tx_chart(request):
    return render(request, 'chart/yearly_tx_chart.html')

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


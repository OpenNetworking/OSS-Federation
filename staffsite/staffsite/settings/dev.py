from .base import *


CHART_API_URL = "http://140.112.29.201:5566/api/v1"
STATISTICS_API_URL = CHART_API_URL

DATABASE_ROUTERS = [
    'chart.ChartRouter.ChartRouter',
    'utils.routers.BaseIssuerRouter',
    'utils.routers.EmailAddressRouter',
]

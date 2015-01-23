import json

from django.conf import settings
import requests



STATISTICS_API_HEADER = getattr(settings, "STATISTICS_API_HEADER", None)
STATISTICS_API_TOKEN = getattr(settings, "STATISTICS_API_TOKEN", None)
STATISTICS_API_URL = getattr(settings, "STATISTICS_API_URL", None)

"""
STATISTICS_API_HEADER = "Authorization"
STATISTICS_API_TOKEN = "Token 44481a014b21de52da066217287a62b02c38eb21"
STATISTICS_API_URL = "http://140.112.29.198:4444/api/v1/statistics"
STATISTICS_API_URL = "http://140.112.29.201:5566/api/v1/statistics"
"""

class StatisticsAPIClient(object):

    def __init__(self, header=STATISTICS_API_HEADER,
                 token=STATISTICS_API_TOKEN, url=STATISTICS_API_URL):
        self.token = token
        self.url = url
        self.headers = {
            STATISTICS_API_HEADER: STATISTICS_API_TOKEN,
            "Content-Type": "application json"
        }

    def _get(self, path, params={}):
        response = requests.get(path, headers=self.headers)
        print dir(response)
        return response

    def get_aeinfo(self, params={}):
        path = self.url + "/aeinfo/"
        if params:
            qs = "?"
            for key, value in params.iteritems():
                qs += key + "=" + value
            path += qs
        return self._get(path)

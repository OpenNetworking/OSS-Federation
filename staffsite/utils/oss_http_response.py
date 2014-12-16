from django.http import (HttpResponse, JsonResponse, HttpResponseBadRequest,
                         HttpResponseNotFound, HttpResponseForbidden,
                         HttpResponseNotAllowed, HttpResponseGone,
                         HttpResponseServerError)
from django.core.serializers.json import DjangoJSONEncoder

class HttpErrResp(HttpResponse):
    """
    An HTTP error response class with specific format
    :param err_code: Error code to be dumped into json.
    :param err_msg: Error message to be dumped into json.
                    Default, Only dict objects are allowed to be passed.
    """

    def __init__(self, err_code, err_msg):
        data = "Error code: %s</br>Error message: %s" % (err_code, err_msg)

        super(HttpErrResp, self).__init__(content=data)

class JsonOkResp(JsonResponse):
    """
    An HTTP json response class with specific format.

    :param data: Data to be dumped into json. Default,
                 Only dict objects are allowed to be passed/
    """

    def __init__(self, data=None, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        data = {'status': 200, 'data': data}
        super(JsonOkResp, self).__init__(data, encoder=encoder, safe=safe, **kwargs)

class JsonErrResp(JsonResponse):
    """
    An HTTP error json response class with specific format

    :param err_code: Error code to be dumped into json.
    :param err_msg: Error message to be dumped into json.
                    Default, Only dict objects are allowed to be passed.
    """

    def __init__(self, err_code, err_msg, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        data = {'status': err_code, 'data': err_msg}
        super(JsonErrResp, self).__init__(data, encoder=encoder, safe=safe, **kwargs)

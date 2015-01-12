from django.shortcuts import render
from django.http import HttpResponse
import logging

from utils.oss_http_response import HttpErrResp
from api_query.api_query import APIClient

logger = logging.getLogger(__name__)

def alliance_list(request):
    """
    list the information of all alliance

    For each alliance, we list
    # alliance address
    # the number of block created by this alliance
    # computing power
    """

    api_client = APIClient()

    try:
        ret = api_client.get_alliances_info()
    except Exception as e:
        err_msg = '%s(%s)' % ('failed to get alliance information', str(e))
        logger.error(err_msg)
        return HttpErrResp(api_client.code, err_msg)

    if api_client.success:
        alliance_list = ret['data']
    else:
        err_msg = '%s(%s)' % ('failed to get alliance information', api_client.err_msg)
        logger.error(err_msg)
        return HttpErrResp(api_client.code, err_msg)

    total_blocks_count = 0
    for alliance in alliance_list:
        total_blocks_count += alliance['block_count']

    ret_alliance_list = []
    for alliance in alliance_list:
        tmp_alliance = {}
        tmp_alliance['address'] = alliance['AE_addr']
        tmp_alliance['created_block'] = alliance['block_count']
        if total_blocks_count == 0:
            tmp_alliance['computing_power'] = 0
        else:
            tmp_alliance['computing_power'] = float(tmp_alliance['created_block']) / float(total_blocks_count) * 100
        ret_alliance_list.append(tmp_alliance)

    return render(request, 'adminapp/alliance_list.html', dict(alliance_list=ret_alliance_list))


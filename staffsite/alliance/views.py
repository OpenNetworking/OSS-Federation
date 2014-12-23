from django.shortcuts import render
from django.http import HttpResponse
from bitcoinrpc import connect_to_local
import logging

import config
from chart.models import Block

logger = logging.getLogger(__name__)

def alliance_list(request):
    """
    list the information of all alliance

    For each alliance, we list
    # alliance address
    # the number of block created by this alliance
    # computing power
    """

    blocks = Block.objects.all()
    all_blocks_count = blocks.count()

    try:
        rpc = connect_to_local(config.BITCOIN_CONF)
        ret = rpc.getmemberlist()

    except Exception as e:
        logger.error(str(e))
        return HttpResponse('failed to get alliance information by rpc call')

    alliance_list = ret['member_list']
    ret_alliance_list = []
    for alliance_addr in alliance_list:
        tmp_alliance = {}
        tmp_alliance['address'] = alliance_addr
        tmp_alliance['created_block'] = Block.objects.filter(block_miner=alliance_addr).count()
        tmp_alliance['computing_power'] = float(tmp_alliance['created_block']) / float(all_blocks_count) * 100
        ret_alliance_list.append(tmp_alliance)

    return render(request, 'adminapp/alliance_list.html', dict(alliance_list=ret_alliance_list))


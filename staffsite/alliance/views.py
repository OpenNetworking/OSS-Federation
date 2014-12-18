from django.shortcuts import render
from bitcoinrpc.connection import BitcoinConnection

import config
from oss.apps.chart.models import Block

logger = logging.getLogger(__name__)

def alliance_list():
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
        rpc = BitcoinConnection(config.RPC_AE_USER,
                                config.RPC_AE_PASSWORD,
                                config.RPC_AE_HOST,
                                config.RPC_AE_PORT)
        ret = rpc.getmemberlist(color.address.address, color.color_id)
    except Exception as e:
        logger.error(str(e))
        return HttpResponse('failed to get alliance information by rpc call')

    alliance_list = ret['member_list']
    ret_alliance_list = []
    for alliance in alliance_list:
        tmp_alliance = {}
        tmp_alliance.address = alliance
        tmp_alliance.created_block = Blocks.objects.filter(block_miner=alliance).count()
        tmp_alliance.computing_power = float(tmp_alliance.created_block) / float(all_blocks_count)
        ret_alliance_list.append(tmp_alliance)

    return render(request, 'adminapp/aliance_list.html', dict(aliance_list=ret_alliance_list))


import urllib
import urllib2
import json

import config

class APIClient(object):

    SUCCESS_CODE = 200

    success = False
    code = 500
    err_msg = ''

    def __init__(self):
        self.api_hosts_list = config.API_SERVERS_CONF_LIST

    def _raise_exception(self, e, code, err_msg):
        self.e = e
        self.code = code
        self.err_msg = "%s (%s)" % (err_msg, str(e))
        raise self.e

    def _send_request(self, query_string):
        for api_conf in self.api_hosts_list:
            url = '%s%s' % (api_conf['url'], query_string)

            try:
                j_resp = json.load(urllib2.urlopen(url))
                self._chk_resp_status(j_resp)
                return j_resp
            except urllib2.HTTPError as e:
                self._raise_exception(e, e.code, 'failed to connect to api server due to http error')
            except urllib2.URLError as e:
                # connection refused
                if e.reason.errno != 111:
                    pass
            except Exception as e:
                self._raise_exception(e, e.code, 'failed to connect to api server')

    def _chk_resp_status(self, j_resp):
        self.code = j_resp['status']

        if self.code == self.SUCCESS_CODE:
            self.success = True
        else:
            self.success = False
            self.err_msg = j_resp['message']

    def get_txs_list(self, **kwargs):
        """
        Get transaction list from api server
        """

        query_data = {}
        query_string = ''

        tx_colors = kwargs.pop('colors', None)
        tx_issuers_addrs = kwargs.pop('issuers_addrs', None)
        tx_date_from = kwargs.pop('date_from', None)
        tx_date_to = kwargs.pop('date_to', None)
        tx_start = kwargs.pop('start', 1)
        tx_end = kwargs.pop('end', 20)
        tx_mode = 0
        query_data['mode'] = tx_mode

        if tx_colors:
            query_data['color'] = tx_colors

        if tx_issuers_addrs:
            query_data['addr'] = tx_issuers_addrs

        if tx_date_from:
            query_data['since'] = tx_date_from
        if tx_date_to:
            query_data['until'] = tx_date_to

        query_data['start'] = tx_start

        query_data['end'] = tx_end

        query_string = '%s%s' % ('tx/?', urllib.urlencode(query_data, doseq=True))

        # remote api call to get txs_list
        try:
            return self._send_request(query_string)
        except Exception as e:
            self._raise_exception(e, '500',
                                  'failed to get response from api server.')

    def get_tx_info(self, tx_id):
        if tx_id is None:
            self._raise_exception(ValueError, '500',
                                  'paraneters are not valid in get transaction info.')

        query_string = '%s%s' % ('transactions?hash=', tx_id)

        try:
            return self._send_request(query_string)
        except Exception as e:
            self._raise_exception(e, '500',
                                  'failed to get transaction info from api server.')

    def get_alliances_info(self):
        query_string = 'statistics/aeinfo/'

        try:
            return self._send_request(query_string)
        except Exception as e:
            self._raise_exception(e, '500',
                                  'failed to get alliances info from api server.')

    def get_issuer_balance(self, colors_list):
        query_data = {}
        query_data['address'] = colors_list
        query_string = '%s%s' % ('sumbalance/?', urllib.urlencode(query_data, doseq=True))

        try:
            return self._send_request(query_string)
        except Exception as e:
            self._raise_exception(e, '500',
                                  'failed to get issuer balance from api server.')


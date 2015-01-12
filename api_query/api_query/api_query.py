import urllib
import urllib2
import json
import abc

import config

class APIClientBase(object):

    __metaclass__ = abc.ABCMeta

    SUCCESS = 200

    # error code
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

    success = False
    code = INTERNAL_SERVER_ERROR
    err_msg = ''

    def __init__(self, query_servers):
        self.api_hosts_list = query_servers

    def _raise_exception(self, e, code, err_msg):
        self.e = e
        self.code = code
        self.err_msg = "%s (%s)" % (err_msg, str(e))
        raise self.e

    def _is_connection_refused(self, exception):
        CONNECTION_REFUSE_CODE = 111

        if exception.reason.errno:
            if exception.reason.errno == CONNECTION_REFUSE_CODE:
                return True

        return False

    def _last_api_conf(self, api_conf, api_conf_list):
        return (api_conf_list[-1] == api_conf)

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
                if self._is_connection_refused(e) and not self._last_api_conf(api_conf, self.api_hosts_list):
                    pass

                self._raise_exception(e, self.INTERNAL_SERVER_ERROR, 'falied to connect to api server')
            except Exception as e:
                self._raise_exception(e, self.INTERNAL_SERVER_ERROR, 'failed to connect to api server')

    @abc.abstractmethod
    def _chk_resp_status(self, j_resp):
        return

class APIClient(APIClientBase):

    def __init__(self):
        super(APIClient, self).__init__(config.GINFO_API_SERVERS)

    def _chk_resp_status(self, j_resp):
        self.code = j_resp['status']

        if self.code == self.SUCCESS:
            self.success = True
        else:
            self.success = False
            self.code = j_resp['status']
            self.err_msg = j_resp['message']


    def get_txs_list(self, **kwargs):
        """
        Get transaction list from api server
        """

        query_data = {}
        query_string = ''

        tx_mode = kwargs.pop('mode', 0)
        tx_colors = kwargs.pop('colors', None)
        tx_licenses_addrs = kwargs.pop('licenses_addrs', None)
        tx_issuers_addrs = kwargs.pop('issuers_addrs', None)
        tx_addrs = kwargs.pop('addrs', None)
        tx_in_addrs = kwargs.pop('in_addrs', None)
        tx_out_addrs = kwargs.pop('out_addrs', None)
        tx_date_from = kwargs.pop('date_from', None)
        tx_date_to = kwargs.pop('date_to', None)
        tx_start = kwargs.pop('start', 1)
        tx_end = kwargs.pop('end', 20)

        query_data['mode'] = tx_mode

        if tx_colors:
            query_data['color'] = tx_colors

        if tx_licenses_addrs:
            query_data['issuer'] = tx_licenses_addrs

        if tx_issuers_addrs:
            query_data['addr'] = tx_issuers_addrs

        if tx_addrs:
            query_data['addr'] = tx_addrs

        if tx_in_addrs:
            query_data['in_addr'] = tx_in_addrs

        if tx_out_addrs:
            query_data['out_addr'] = tx_out_addrs

        if tx_date_from:
            query_data['since'] = tx_date_from
        if tx_date_to:
            query_data['until'] = tx_date_to

        query_data['start'] = tx_start

        query_data['end'] = tx_end

        if tx_licenses_addrs:
            query_string = '%s%s' % ('tx/license/?', urllib.urlencode(query_data, doseq=True))
        else:
            query_string = '%s%s' % ('tx/?', urllib.urlencode(query_data, doseq=True))

        try:
            return self._send_request(query_string)
        except Exception as e:
            self._raise_exception(e, self.INTERNAL_SERVER_ERROR,
                                  'failed to get response from api server.')

    def get_tx_info(self, tx_id):
        if tx_id is None:
            self._raise_exception(ValueError, self.INTERNAL_SERVER_ERROR,
                                  'paraneters are not valid in get transaction info.')

        query_string = '%s%s' % ('transactions?hash=', tx_id)

        try:
            return self._send_request(query_string)
        except Exception as e:
            self._raise_exception(e, self.INTERNAL_SERVER_ERROR,
                                  'failed to get transaction info from api server.')

    def get_alliances_info(self):
        query_string = 'statistics/aeinfo/'

        try:
            return self._send_request(query_string)
        except Exception as e:
            self._raise_exception(e, self.INTERNAL_SERVER_ERROR,
                                  'failed to get alliances info from api server.')

    def get_balance(self, addresses_list):
        query_data = {}
        query_data['address'] = addresses_list
        query_string = '%s%s' % ('sumbalance/?', urllib.urlencode(query_data, doseq=True))

        try:
            return self._send_request(query_string)
        except Exception as e:
            self._raise_exception(e, self.INTERNAL_SERVER_ERROR,
                                  'failed to get issuer balance from api server.')

    def get_orphan_blk(self, **kwargs):
        query_data = {}
        query_string = ''

        time_since = kwargs.pop('since', None)
        time_until = kwargs.pop('until', None)

        if time_since:
            query_data['since'] = time_since
        if time_until:
            query_data['until'] = time_until

        query_string = '%s%s' % ('statistics/orphan/?', urllib.urlencode(query_data, doseq=True))

        try:
            return self._send_request(query_string)
        except Exception as e:
            self._raise_exception(e, self.INTERNAL_SERVER_ERROR,
                                  'failed to get orphan block information from api server.')


"""
Copyright © 2020-2021 FC Tools.
All rights reserved.
Author: German Yakimov
"""

import requests
import json
from ts_clients.base_client import TrafficSourceClient


class PropellerClient(TrafficSourceClient):
    def __init__(self):
        self._base_requests_url = 'https://ssp-api.propellerads.com/v5/adv/'

        super().__init__()

    def start_campaign(self, campaign_id, api_key):
        requests_url = self._base_requests_url + 'campaigns/play'
        response = requests.put(requests_url, data=json.dumps({'campaign_ids': [int(campaign_id)]}))

    def stop_campaign(self, campaign_id, api_key):
        requests_url = self._base_requests_url + 'campaigns/stop'
        response = requests.put(requests_url, data=json.dumps({'campaign_ids': [int(campaign_id)]}))

    def add_site_to_black_list(self, site_id, api_key):
        raise NotImplemented()

    def add_site_to_white_list(self, site_id, api_key):
        raise NotImplemented()

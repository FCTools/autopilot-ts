# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import requests
import json
from ts_clients.base_client import TrafficSourceClient


class PropellerClient(TrafficSourceClient):
    def __init__(self):
        self._base_requests_url = 'https://ssp-api.propellerads.com/v5/adv/'

        super().__init__()

    def start_campaign(self, campaign_id, api_key):
        requests_url = self._base_requests_url + 'campaigns/play'
        data = json.dumps({"campaign_ids": [int(campaign_id)]})
        response = requests.put(requests_url, data=data,
                                headers={"Authorization": f"Bearer {api_key}",
                                         "Accept": "application/json", "Content-Type": "application/json"}
                                )

    def stop_campaign(self, campaign_id, api_key):
        requests_url = self._base_requests_url + 'campaigns/stop'
        data = json.dumps({"campaign_ids": [int(campaign_id)]})
        response = requests.put(requests_url, data=data,
                                headers={"Authorization": f"Bearer {api_key}",
                                         "Accept": "application/json", "Content-Type": "application/json"}
                                )

    def add_site_to_black_list(self, site_id, api_key):
        raise NotImplemented()

    def add_site_to_white_list(self, site_id, api_key):
        raise NotImplemented()

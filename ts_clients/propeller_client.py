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

    def change_campaign_status(self, campaign_id, api_key, status):
        if status == 'stop':
            requests_url = self._base_requests_url + 'campaigns/stop'
        elif status == 'play':
            requests_url = self._base_requests_url + 'campaigns/play'
        else:
            return

        response = requests.put(requests_url, data=json.dumps({"campaign_ids": [int(campaign_id)]}),
                                headers={"Authorization": f"Bearer {api_key}",
                                         "Accept": "application/json", "Content-Type": "application/json"}
                                )

    def add_zones_to_list(self, campaign_id, zones_list, api_key, list_type):
        if list_type == 'black':
            requests_url = self._base_requests_url + f'campaigns/{campaign_id}/targeting/exclude/zone'
        elif list_type == 'white':
            requests_url = self._base_requests_url + f'campaigns/{campaign_id}/targeting/include/zone'
        else:
            return

        current_zones_list = set(requests.get(requests_url, params={'campaignId': str(campaign_id)},
                                              headers={"Authorization": f"Bearer {api_key}",
                                                       "Accept": "application/json", "Content-Type": "application/json"}
                                              ).json()['zone'])
        start_len = len(current_zones_list)

        for zone in zones_list:
            current_zones_list.add(zone)

        if len(current_zones_list) != start_len:
            data = json.dumps({"zone": list(current_zones_list)})
            response = requests.put(requests_url, data=data, params={'campaignId': str(campaign_id)},
                                    headers={"Authorization": f"Bearer {api_key}",
                                             "Accept": "application/json", "Content-Type": "application/json"})

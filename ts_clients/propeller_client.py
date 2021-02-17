# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import json

import requests

from helpers import requests_manager
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
            return f'Incorrect status given: {status}'

        response = requests_manager.put(requests.Session(), requests_url,
                                        data=json.dumps({"campaign_ids": [int(campaign_id)]}),
                                        headers={"Authorization": f"Bearer {api_key}",
                                                 "Accept": "application/json", "Content-Type": "application/json"})

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to change campaign status in propeller: {response}'

        return 'OK'

    def add_zones_to_list(self, campaign_id, zones_list, api_key, list_type):
        if list_type == 'black':
            requests_url = self._base_requests_url + f'campaigns/{campaign_id}/targeting/exclude/zone'
        elif list_type == 'white':
            requests_url = self._base_requests_url + f'campaigns/{campaign_id}/targeting/include/zone'
        else:
            return

        response = requests_manager.get(requests.Session(), requests_url, params={'campaignId': str(campaign_id)},
                                        headers={"Authorization": f"Bearer {api_key}",
                                                 "Accept": "application/json", "Content-Type": "application/json"})

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to get campaign {list_type} list: {response}'

        current_zones_list = set(response.json()['zone'])
        zones_to_add = set()

        for zone in zones_list:
            if zone not in current_zones_list:
                zones_to_add.add(zone)

        if len(zones_to_add) != 0:
            response = requests_manager.put(requests.Session(), requests_url,
                                            data=json.dumps({"zone": list(zones_to_add)}),
                                            params={'campaignId': str(campaign_id)},
                                            headers={"Authorization": f"Bearer {api_key}",
                                                     "Accept": "application/json", "Content-Type": "application/json"})
            if not isinstance(response, requests.Response):
                return f'Error occurred while trying to set campaign {list_type} list: {response}'

        return 'OK'

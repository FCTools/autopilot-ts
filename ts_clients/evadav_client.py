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


class EvadavClient(TrafficSourceClient):
    def __init__(self):
        self._base_requests_url = 'https://evadav.com/api/v2.0'

        super().__init__()

    def change_campaign_status(self, campaign_id, api_key, status):
        if status == 'stop':
            requests_url = self._base_requests_url + '/advertiser/campaigns/stop'
        elif status == 'play':
            requests_url = self._base_requests_url + '/advertiser/campaigns/activate'
        else:
            return f'Incorrect status given: {status}'

        response = requests_manager.put(requests.Session(), requests_url,
                                        params={"access-token": api_key,
                                                "id": campaign_id},
                                        headers={"Accept": "application/json",
                                                 "Content-Type": "application/json"})

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to change campaign status in evadav: {response}'

        return 'OK'

    def add_zones_to_list(self, campaign_id, zones_list, api_key, list_type=None,
                          list_to_add=None):
        requests_url = self._base_requests_url + '/advertiser/sources/add'

        response = requests_manager.post(requests.Session(), requests_url,
                                         params={"access-token": api_key},
                                         headers={"Accept": "application/json",
                                                  "Content-Type": "application/json"},
                                         data=json.dumps({"audience": list_to_add,  # check this
                                                          "sources": list(zones_list)}))

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to add zones to audience in evadav: {response}'

        return 'OK'

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
from helpers.consts import *
from ts_clients.base_client import TrafficSourceClient

class VimmyClient(TrafficSourceClient):
    def __init__(self):
        self._base_requests_url = VIMMY_URL

        super().__init__()

    def change_campaign_status(self, campaign_id, api_key, status, client_key=None):
        requests_url = self._base_requests_url + f'campaigns/{campaign_id}?api_key={api_key}'

        response = requests_manager.put(requests.Session(), requests_url,
                                        data=json.dumps({'status': 0 if status == STOP else 1}))

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to change campaign status in Vimmy: {response}'

        if response.status_code != 200:
            return f'Non-success status code occurred while trying to ' \
                f'change campaign status in Vimmy: {response.content}'

        return 'OK'

    def add_zones_to_list(self, campaign_id, zones_list, api_key, list_type=None,
        list_to_add=None, client_key=None):
        NotImplemented
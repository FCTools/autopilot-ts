# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from ts_clients.base_client import TrafficSourceClient
from helpers import requests_manager
import requests


class MGIDClient(TrafficSourceClient):
    def __init__(self):
        self._base_requests_url = 'https://api.mgid.com/v1/goodhits/clients/'

        super().__init__()

    def change_campaign_status(self, campaign_id, api_key, status, client_id=None):
        requests_url = self._base_requests_url + f'{client_id}/campaigns/{campaign_id}/'

        params = {
            'token': api_key,
            'whetherToBlockByClient': 1 if status == 'stop' else 0
        }

        response = requests_manager.patch(requests.Session(), requests_url, params=params)

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to change campaign status in mgid: {response}'

        if response.status_code != 200:
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in mgid: {response.content}'

        return 'OK'

    def add_zones_to_list(self, campaign_id, zones_list, api_key, list_type=None,
                          list_to_add=None):
        raise NotImplemented()

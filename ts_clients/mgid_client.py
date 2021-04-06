# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import requests

from helpers import requests_manager
from helpers.consts import *
from ts_clients.base_client import TrafficSourceClient


class MGIDClient(TrafficSourceClient):
    def __init__(self):
        self._base_requests_url = MGID_URL

        super().__init__()

    def change_campaign_status(self, campaign_id, api_key, status, client_key=None):
        requests_url = self._base_requests_url + f'{client_key}/campaigns/{campaign_id}/'

        params = {
            'token': api_key,
            'whetherToBlockByClient': 1 if status == STOP else 0
        }

        response = requests_manager.patch(requests_url, params=params)

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to change campaign status in mgid: {response}'

        if response.status_code != 200:
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in mgid: {response.content}'

        return 'OK'

    def add_zones_to_list(self, campaign_id, zones_list, api_key, list_type=None,
                          list_to_add=None, client_key=None):
        requests_url = self._base_requests_url + f'{client_key}/campaigns/{campaign_id}'

        editing_method = 'include' if list_type == WHITELIST else 'exclude'
        filter_type = 'only'
        zones = ','.join(zones_list)

        params = {
            'token': api_key,
            'widgetsFilterUid': f'{editing_method}, {filter_type}, {zones}'
        }

        print(params)

        response = requests_manager.patch(requests_url, params=params)

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to add zones to audience in mgid: {response}'

        if response.status_code != 200:
            return f'Non-success status code occurred while trying to ' \
                   f'add zones to audience in mdid: {response.content}'

        print(response.text)

        return 'OK'

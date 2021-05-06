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
from helpers.db_logger import Logger
from ts_clients.base_client import TrafficSourceClient


class VimmyClient(TrafficSourceClient):
    def __init__(self):
        self._base_requests_url = VIMMY_URL
        self._logger = Logger()

        super().__init__()

    def change_campaign_status(self, task_id, campaign_id, api_key, status, client_key=None):
        headers = {'content-type': 'application/json', 'accept': 'application/json', 'X-Api-Key': api_key}
        requests_url = self._base_requests_url + f'campaigns/{campaign_id}'

        campaign_info = requests_manager.get(requests_url, headers=headers)

        # TODO: log response here and all requests details

        if not isinstance(campaign_info, requests.Response):
            return f'Error occurred while trying to change campaign status in Vimmy: {campaign_info}'

        if campaign_info.status_code != HTTP_200_SUCCESS:
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in Vimmy: {campaign_info.content}'

        campaign_data = json.loads(campaign_info.text)
        campaign_data['status'] = 2 if status == STOP else 1

        response = requests_manager.put(requests_url,
                                        data=json.dumps(campaign_data, ensure_ascii=False).encode('utf-8'),
                                        headers=headers)

        # TODO: log response here and all requests details

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to change campaign status in Vimmy: {response}'

        if response.status_code != HTTP_200_SUCCESS:
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in Vimmy: {response.content}'

        return 'OK'

    def add_zones_to_list(self, task_id, campaign_id, zones_list, api_key, list_type=None, list_to_add=None, client_key=None):
        headers = {'content-type': 'application/json', 'accept': 'application/json', 'X-Api-Key': api_key}

        requests_url = self._base_requests_url + f'campaigns/{campaign_id}'
        campaign_info = requests_manager.get(requests_url, headers=headers)

        # TODO: log response here and all requests details

        if not isinstance(campaign_info, requests.Response):
            return f'Error occurred while trying to change campaign status in Vimmy: {campaign_info}'

        if campaign_info.status_code != HTTP_200_SUCCESS:
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in Vimmy: {campaign_info.content}'

        campaign_data = campaign_info.json()
        campaign_data['sites']['is_white'] = (list_type == WHITELIST)
        campaign_data['sites']['items'] = zones_list

        response = requests_manager.put(requests_url, data=json.dumps(campaign_data).encode('utf-8'), headers=headers)

        # TODO: log response here and all requests details

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to change campaign status in Vimmy: {response}'

        if response.status_code != HTTP_200_SUCCESS:
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in Vimmy: {response.content}'

        return 'OK'

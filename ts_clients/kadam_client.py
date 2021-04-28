# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>
import json
import logging
import os

import requests

from helpers import requests_manager
from helpers.consts import *
from ts_clients.base_client import TrafficSourceClient


class KadamClient(TrafficSourceClient):
    def __init__(self):
        self._base_requests_url = KADAM_URL

        super().__init__()
        self._setup_logger('kadam')

    def change_campaign_status(self, campaign_id, api_key, status, client_id=None):
        requests_url = self._base_requests_url + f'ads.campaigns.update/'

        response = requests_manager.patch(requests_url,
                                          data=json.dumps({'data': [{'campaign_id': campaign_id,
                                                           'status': 0 if status == STOP else 1}]}))

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to change campaign status in kadam: {response}'

        if response.status_code != HTTP_200_SUCCESS:
            self._logger.error(response.text)
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in kadam: {response.content}'

        return 'OK'

    def add_zones_to_list(self, campaign_id, zones_list, api_key, list_type=None, list_to_add=None, client_key=None):
        requests_url = self._base_requests_url + f'ads.campaigns.update/'

        if list_type == BLACKLIST:
            response = requests_manager.patch(requests_url,
                                              data=json.dumps({'data': [{'campaign_id': campaign_id,
                                                                         'black_list': zones_list}]}))

        if list_type == WHITELIST:
            response = requests_manager.patch(requests_url,
                                              data=json.dumps({'data': [{'campaign_id': campaign_id,
                                                                         'white_list': zones_list}]}))
        else:
            return f'Incorrect list type: {list_type}'

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to change campaign status in kadam: {response}'

        if response.status_code != HTTP_200_SUCCESS:
            self._logger.error(response.text)
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in kadam: {response.content}'

        return 'OK'

# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import json
from datetime import datetime
from hashlib import md5
from urllib.parse import urlencode

import requests

from helpers import requests_manager
from helpers.consts import *
from helpers.db_logger import Logger
from ts_clients.base_client import TrafficSourceClient


class KadamClient(TrafficSourceClient):
    def __init__(self):
        self._base_requests_url = KADAM_URL
        self._logger = Logger()

        super().__init__()

    def change_campaign_status(self, task_id, campaign_id, api_key, status, client_key=None):
        requests_url = self._base_requests_url + f'ads.campaigns.update/'
        signature = md5(f'. {api_key}'.encode(encoding='utf-8'))
        params = {'signature': signature, 'data': json.dumps({'data': [{'campaign_id': campaign_id,
                                                                        'status': 0 if status == STOP else 1}]}),
                  'client_id': client_key}

        response = requests_manager.patch(requests_url, params=params)

        if not isinstance(response, requests.Response):
            self._logger.log_request(task_id, time_=str(datetime.now()), request_url=requests_url + urlencode(params),
                                     headers='-', body='null', type_='PATCH', response=str(response),
                                     status_code=-1, description='request to change campaign status in kadam')

            return f'Error occurred while trying to change campaign status in kadam: {response}'

        self._logger.log_request(task_id, time_=str(datetime.now()), request_url=requests_url + urlencode(params),
                                 headers='-', body='null', type_='PATCH', response=str(response.text),
                                 status_code=response.status_code,
                                 description='request to change campaign status in kadam')

        if response.status_code != HTTP_200_SUCCESS:
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in kadam: {response.content}'

        return 'OK'

    def add_zones_to_list(self, task_id, campaign_id, zones_list, api_key, list_type=None, list_to_add=None,
                          client_key=None):
        requests_url = self._base_requests_url + f'ads.campaigns.update/'

        signature = md5(f'. {api_key}'.encode(encoding='utf-8'))
        params = {'signature': signature, 'client_id': client_key}

        if list_type == BLACKLIST:
            data = json.dumps({'data': [{'campaign_id': campaign_id, 'black_list': zones_list}]})
        elif list_type == WHITELIST:
            data = json.dumps({'data': [{'campaign_id': campaign_id, 'white_list': zones_list}]})
        else:
            return f'Incorrect list type: {list_type}'

        params['data'] = data

        response = requests_manager.patch(requests_url, params=params)

        if not isinstance(response, requests.Response):
            self._logger.log_request(task_id, time_=str(datetime.now()), request_url=requests_url + urlencode(params),
                                     headers='-', body='null', type_='PATCH', response=str(response),
                                     status_code=-1,
                                     description='request to add zones to list in kadam')

            return f'Error occurred while trying to change campaign status in kadam: {response}'

        self._logger.log_request(task_id, time_=str(datetime.now()), request_url=requests_url + urlencode(params),
                                 headers='-', body='null', type_='PATCH', response=str(response.text),
                                 status_code=response.status_code,
                                 description='request to add zones to list in kadam')

        if response.status_code != HTTP_200_SUCCESS:
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in kadam: {response.content}'

        return 'OK'

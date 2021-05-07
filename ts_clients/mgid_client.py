# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from datetime import datetime
from urllib.parse import urlencode

import requests

from helpers import requests_manager
from helpers.consts import *
from helpers.db_logger import Logger
from ts_clients.base_client import TrafficSourceClient


class MGIDClient(TrafficSourceClient):
    def __init__(self):
        self._base_requests_url = MGID_URL
        self._logger = Logger()

        super().__init__()

    def change_campaign_status(self, task_id, campaign_id, api_key, status, client_key=None):
        requests_url = self._base_requests_url + f'{client_key}/campaigns/{campaign_id}/'

        params = {
            'token': api_key,
            'whetherToBlockByClient': 1 if status == STOP else 0
        }

        response = requests_manager.patch(requests_url, params=params)

        # prevent token leak from logs
        params['token'] = 'token'

        if not isinstance(response, requests.Response):
            self._logger.log_request(task_id, time_=str(datetime.now()),
                                     request_url=requests_url.replace(client_key, 'client_id') + urlencode(params),
                                     headers='-', body='null', type_='PATCH', response=str(response),
                                     status_code=-1,
                                     description='request to change campaign status in mgid')

            return f'Error occurred while trying to change campaign status in mgid: {response}'

        self._logger.log_request(task_id, time_=str(datetime.now()),
                                 request_url=requests_url.replace(client_key, 'client_id') + urlencode(params),
                                 headers='-', body='null', type_='PATCH', response=str(response.text),
                                 status_code=response.status_code,
                                 description='request to change campaign status in mgid')

        if response.status_code != HTTP_200_SUCCESS:
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in mgid: {response.content}'

        return 'OK'

    def add_zones_to_list(self, task_id, campaign_id, zones_list, api_key, list_type=None,
                          list_to_add=None, client_key=None):
        requests_url = self._base_requests_url + f'{client_key}/campaigns/{campaign_id}'
        editing_method = 'include' if list_type == WHITELIST else 'exclude'
        filter_type = 'off'
        zones = ','.join(zones_list)

        params = {
            'token': api_key
        }
        requests_url_tmp = requests_url + f'?widgetsFilterUid={editing_method}, off'
        response = requests.patch(requests_url_tmp, params=params)

        # prevent token leak from logs
        params_ = {'token': 'token'}

        if not isinstance(response, requests.Response):
            self._logger.log_request(task_id, time_=str(datetime.now()),
                                     request_url=requests_url_tmp.replace(client_key, 'client_id') + urlencode(params_),
                                     headers='-', body='null', type_='PATCH', response=str(response),
                                     status_code=-1,
                                     description='request to change filter type in mgid')

            return f'Error occurred while trying to add zones to audience in mgid: {response}'

        self._logger.log_request(task_id, time_=str(datetime.now()),
                                 request_url=requests_url_tmp.replace(client_key, 'client_id') + urlencode(params_),
                                 headers='-', body='null', type_='PATCH', response=str(response.text),
                                 status_code=response.status_code,
                                 description='request to change filter type in mgid')

        if response.status_code != HTTP_200_SUCCESS:
            return f'Non-success status code occurred while trying to ' \
                   f'add zones to audience in mgid: {response.content}'

        requests_url += f'?widgetsFilterUid={editing_method}, {filter_type}, {zones}'

        response = requests_manager.patch(requests_url, params=params)

        if not isinstance(response, requests.Response):
            self._logger.log_request(task_id, time_=str(datetime.now()),
                                     request_url=requests_url.replace(client_key, 'client_id') + urlencode(params_),
                                     headers='-', body='null', type_='PATCH', response=str(response),
                                     status_code=-1,
                                     description='request to add zones to list in mgid')
            return f'Error occurred while trying to add zones to audience in mgid: {response}'

        self._logger.log_request(task_id, time_=str(datetime.now()),
                                 request_url=requests_url.replace(client_key, 'client_id') + urlencode(params_),
                                 headers='-', body='null', type_='PATCH', response=str(response.text),
                                 status_code=response.status_code,
                                 description='request to add zones to list in mgid')

        if response.status_code != HTTP_200_SUCCESS:
            return f'Non-success status code occurred while trying to ' \
                   f'add zones to audience in mgid: {response.content}'

        return 'OK'

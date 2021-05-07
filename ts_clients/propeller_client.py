# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import json
from datetime import datetime
from urllib.parse import urlencode

import requests

from helpers import requests_manager
from helpers.consts import *
from helpers.db_logger import Logger
from ts_clients.base_client import TrafficSourceClient


class PropellerClient(TrafficSourceClient):
    def __init__(self):
        self._base_requests_url = PROPELLER_URL
        self._logger = Logger()

        super().__init__()

    def change_campaign_status(self, task_id, campaign_id, api_key, status, client_key=None):
        if status == STOP:
            requests_url = self._base_requests_url + 'campaigns/stop'
        elif status == PLAY:
            requests_url = self._base_requests_url + 'campaigns/play'
        else:
            return f'Incorrect status given: {status}'

        data = json.dumps({"campaign_ids": [int(campaign_id)]})
        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json",
                   "Content-Type": "application/json"}

        response = requests_manager.put(requests_url, data=data, headers=headers)

        if not isinstance(response, requests.Response):
            self._logger.log_request(task_id, time_=str(datetime.now()), request_url=requests_url,
                                     headers=json.dumps(headers), body=data, type_='PUT', response=str(response),
                                     status_code=-1,
                                     description='request to change campaign status in propeller')

            return f'Error occurred while trying to change campaign status in propeller: {response}'

        self._logger.log_request(task_id, time_=str(datetime.now()), request_url=requests_url,
                                 headers=json.dumps(headers), body=data, type_='PUT', response=str(response.text),
                                 status_code=response.status_code,
                                 description='request to change campaign status in propeller')

        if response.status_code != HTTP_200_SUCCESS:
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in propeller: {response.content}'

        return 'OK'

    def add_zones_to_list(self, task_id, campaign_id, zones_list, api_key, list_type=None, list_to_add=None,
                          client_key=None):
        if list_type == BLACKLIST:
            requests_url = self._base_requests_url + f'campaigns/{campaign_id}/targeting/exclude/zone'
        elif list_type == WHITELIST:
            requests_url = self._base_requests_url + f'campaigns/{campaign_id}/targeting/include/zone'
        else:
            return f'Incorrect list in propeller: {list_type}'

        params = {'campaignId': str(campaign_id)}
        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json",
                   "Content-Type": "application/json"}

        response = requests_manager.get(requests_url, params=params, headers=headers)

        # TODO: log response here and all requests details

        if not isinstance(response, requests.Response):
            self._logger.log_request(task_id, time_=str(datetime.now()), request_url=requests_url + urlencode(params),
                                     headers=json.dumps(headers), body='null', type_='GET', response=str(response),
                                     status_code=-1,
                                     description='request to get zones already included/excluded zones from propeller')

            return f'Error occurred while trying to get campaign {list_type} list: {response}'

        self._logger.log_request(task_id, time_=str(datetime.now()), request_url=requests_url + urlencode(params),
                                 headers=json.dumps(headers), body='null', type_='GET', response=str(response.text),
                                 status_code=response.status_code,
                                 description='request to get zones already included/excluded zones from propeller')

        if response.status_code != HTTP_200_SUCCESS:
            return f'Non-success status code occurred while trying to get campaign {list_type} list: {response.content}'

        try:
            current_zones_list = set(response.json()['zone'])
        except json.decoder.JSONDecodeError as error:
            return f'Json decode error: {error.doc}'

        current_zones_list.update(zones_list)

        if len(current_zones_list) != 0:
            data = json.dumps({"zone": list(current_zones_list)})
            params = {'campaignId': str(campaign_id)}
            headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json",
                       "Content-Type": "application/json"}

            response = requests_manager.put(requests_url, data=data, params=params, headers=headers)

            # TODO: log response here and all requests details

            if not isinstance(response, requests.Response):
                self._logger.log_request(task_id, time_=str(datetime.now()),
                                         request_url=requests_url + urlencode(params),
                                         headers=json.dumps(headers), body=data, type_='PUT',
                                         response=str(response),
                                         status_code=-1,
                                         description='request to include/exclude zones in propeller')

                return f'Error occurred while trying to set campaign {list_type} list: {response}'

            self._logger.log_request(task_id, time_=str(datetime.now()), request_url=requests_url + urlencode(params),
                                     headers=json.dumps(headers), body=data, type_='PUT', response=str(response.text),
                                     status_code=response.status_code,
                                     description='request to include/exclude zones in propeller')

            if response.status_code != HTTP_200_SUCCESS:
                return f'Non-success status code occurred while trying to ' \
                       f'add zones to list in propeller: {response.content}'

        return 'OK'

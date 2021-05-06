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


class EvadavClient(TrafficSourceClient):
    def __init__(self):
        self._base_requests_url = EVADAV_URL

        super().__init__()
        self._setup_logger('evadav')

    # TODO: add task_id to arguments
    def _get_campaign_status(self, campaign_id, api_key):
        requests_url = self._base_requests_url + '/advertiser/campaigns/get'

        response = requests_manager.get(requests_url,
                                        params={"access-token": api_key,
                                                "id": campaign_id},
                                        headers={"Accept": "application/json",
                                                 "Content-Type": "application/json"})

        # TODO: log response here and all requests details
        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to change campaign status in evadav: {response}'

        if response.status_code != HTTP_200_SUCCESS:
            self._logger.error(response.text)
            return f'Non-success status code occurred while trying to change status in evadav: {response.text}'

        try:
            response = response.json()
            self._logger.info(response)

            if response['success']:
                return response['data']['campaign']['status']
            else:
                return 'error'
        except Exception:
            return 'error'

    # TODO: add task_id to arguments
    def change_campaign_status(self, campaign_id, api_key, status, client_key=None):
        if status == STOP:
            requests_url = self._base_requests_url + '/advertiser/campaigns/stop'
        elif status == PLAY:
            requests_url = self._base_requests_url + '/advertiser/campaigns/activate'
        else:
            return f'Incorrect status given: {status}'

        campaign_status = self._get_campaign_status(campaign_id, api_key)
        if campaign_status == 'error':
            return f"Can't get current campaign status: {campaign_id}"

        if status == STOP and campaign_status == 'stopped':
            return 'OK'
        if status == PLAY and campaign_status == 'active':
            return 'OK'

        response = requests_manager.post(requests_url,
                                         params={"access-token": api_key,
                                                 "id": campaign_id},
                                         headers={"Accept": "application/json",
                                                  "Content-Type": "application/json"})

        # TODO: log response here and all requests details

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to change campaign status in evadav: {response}'

        if response.status_code != HTTP_200_SUCCESS:
            self._logger.error(response.text)
            return f'Non-success status code occurred while trying to change status in evadav: {response.text}'

        return 'OK'

    # TODO: add task_id to arguments
    def add_zones_to_list(self, campaign_id, zones_list, api_key, list_type=None, list_to_add=None, client_key=None):
        requests_url = self._base_requests_url + '/advertiser/sources/add'

        response = requests_manager.post(requests_url,
                                         params={"access-token": api_key},
                                         headers={"Accept": "application/json",
                                                  "Content-Type": "application/json"},
                                         data=json.dumps({"audience": list_to_add,
                                                          "sources": list(zones_list)}))

        # TODO: log response here and all requests details

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to add zones to audience in evadav: {response}'

        if response.status_code != HTTP_200_SUCCESS:
            self._logger.error(response.text)
            return f'Non-success status code occurred while trying to ' \
                   f'add zones to audience in evadav: {response.content}'

        return 'OK'

# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import json
from hashlib import md5

import requests

from helpers import requests_manager
from helpers.consts import *
from ts_clients.base_client import TrafficSourceClient


class KadamClient(TrafficSourceClient):
    def __init__(self):
        self._base_requests_url = KADAM_URL

        super().__init__()
        self._setup_logger('kadam')

    def _generate_api_key(self, data):
        app_id = data['app_id']
        secret_key = data['secret_key']

        response = requests_manager.get('http://api.kadam.net/auth.token', params={'app_id': app_id,
                                                                                   'secret_key': secret_key})

        if not isinstance(response, requests.Response):
            return False, f'Error occurred while trying to generate access_token in kadam: {response}'

        if response.status_code != HTTP_200_SUCCESS:
            self._logger.error(response.text)
            return False, f'Error occurred while trying to generate access_token in kadam: {response.content}'

        try:
            access_token = response.json()['access_token']
            return True, access_token
        except json.JSONDecodeError as exc:
            self._logger.error(f'Error occurred while trying to decode kadam response (access_token generating): {exc.doc}')
            return False, '-'
        except KeyError:
            self._logger.error(f"Can't find field access_token in kadam-response (access_token generating): {response.json()}")
            return False, '-'

    def change_campaign_status(self, campaign_id, api_key, status, client_key=None):
        success, api_key = self._generate_api_key(api_key)

        if not success:
            return "Can't generate kadam access_token"

        requests_url = self._base_requests_url + f'ads.campaigns.update/'

        signature = md5(f'. {api_key}'.encode(encoding='utf-8'))
        params = {'signature': signature, 'data': json.dumps({'data': [{'campaign_id': campaign_id,
                                                                        'status': 0 if status == STOP else 1}]}),
                  'client_id': client_key}

        response = requests_manager.patch(requests_url, params=params)

        # TODO: log response here and all requests details

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to change campaign status in kadam: {response}'

        if response.status_code != HTTP_200_SUCCESS:
            self._logger.error(response.text)
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in kadam: {response.content}'

        return 'OK'

    def add_zones_to_list(self, campaign_id, zones_list, api_key, list_type=None, list_to_add=None, client_key=None):
        success, api_key = self._generate_api_key(api_key)

        if not success:
            return "Can't generate kadam access_token"

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

        # TODO: log response here and all requests details

        if not isinstance(response, requests.Response):
            return f'Error occurred while trying to change campaign status in kadam: {response}'

        if response.status_code != HTTP_200_SUCCESS:
            self._logger.error(response.text)
            return f'Non-success status code occurred while trying to ' \
                   f'change campaign status in kadam: {response.content}'

        return 'OK'

"""
Copyright © 2020-2021 FC Tools.
All rights reserved.
Author: German Yakimov
"""

from ts_clients.propeller_client import PropellerClient


class UpdatesHandler:
    def __init__(self):
        self._propeller_client = PropellerClient()

    def handle(self, update):
        key, value = update

        # log key for task

        if value['ts'] == 'prop':
            if value['action'] == 'start':
                self._propeller_client.start_campaign(value['campaign_id'], value['api_key'])
            elif value['action'] == 'stop':
                self._propeller_client.stop_campaign(value['campaign_id'], value['api_key'])

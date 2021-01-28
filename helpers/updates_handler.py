# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from ts_clients.propeller_client import PropellerClient

# actions defines
PLAY_CAMPAIGN = 1
STOP_CAMPAIGN = 2
EXCLUDE_ZONE = 3
INCLUDE_ZONE = 4


class UpdatesHandler:
    def __init__(self):
        self._propeller_client = PropellerClient()

    def handle(self, update):
        if update['ts'] == 'Propeller Ads':
            if update['action'] == PLAY_CAMPAIGN:
                status = self._propeller_client.change_campaign_status(update['campaign_id'], update['api_key'],
                                                                       status='play')
            elif update['action'] == STOP_CAMPAIGN:
                status = self._propeller_client.change_campaign_status(update['campaign_id'], update['api_key'],
                                                                       status='stop')
            elif update['action'] == EXCLUDE_ZONE:
                status = self._propeller_client.add_zones_to_list(update['campaign_id'], update['zones'],
                                                                  update['api_key'], list_type='black')
            elif update['action'] == INCLUDE_ZONE:
                status = self._propeller_client.add_zones_to_list(update['campaign_id'], update['zones'],
                                                                  update['api_key'], list_type='white')
            else:
                return f"Unknown action: {update['action']}"
        else:
            return f"Unknown traffic source: {update['ts']}"

        return status

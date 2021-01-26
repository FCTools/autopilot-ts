# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from ts_clients.propeller_client import PropellerClient


class UpdatesHandler:
    def __init__(self):
        self._propeller_client = PropellerClient()

    def handle(self, update):
        if update['ts'] == 'Propeller Ads':
            if update['action'] == 1:
                self._propeller_client.start_campaign(update['campaign_id'], update['api_key'])
            elif update['action'] == 2:
                self._propeller_client.stop_campaign(update['campaign_id'], update['api_key'])
            elif update['action'] == 3:
                self._propeller_client.add_zones_to_black_list(update['campaign_id'], update['zones_list'],
                                                               update['api_key'])
            elif update['action'] == 4:
                self._propeller_client.add_zones_to_white_list(update['campaign_id'], update['zones_list'],
                                                               update['api_key'])

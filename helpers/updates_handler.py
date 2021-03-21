# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import logging

from pydantic import ValidationError

from helpers.consts import *
from ts_clients.evadav_client import EvadavClient
from ts_clients.mgid_client import MGIDClient
from ts_clients.propeller_client import PropellerClient
from ts_clients.update import Update

_logger = logging.getLogger(__name__)


class UpdatesHandler:
    def __init__(self):
        self._propeller_client = PropellerClient()
        self._evadav_client = EvadavClient()
        self._mgid_client = MGIDClient()

    def handle(self, update):
        status = None

        try:
            update = Update(**update)
        except ValidationError:
            return f'Incorrect update: {update}'

        if update.ts == PROPELLER_ADS:
            client = self._propeller_client
        elif update.ts == EVADAV:
            client = self._evadav_client
        elif update.ts == MGID:
            client = self._mgid_client
        else:
            return f"Unknown traffic source: {update.ts}"

        if update.action == PLAY_CAMPAIGN:
            status = client.change_campaign_status(update.campaign_id, update.api_key,
                                                   status=PLAY)
        elif update.action == STOP_CAMPAIGN:
            status = client.change_campaign_status(update.campaign_id, update.api_key,
                                                   status=STOP)
        elif update.action == EXCLUDE_ZONE:
            if isinstance(client, PropellerClient):
                status = client.add_zones_to_list(update.campaign_id, update.zones,
                                                  update.api_key, list_type=BLACKLIST)
            elif isinstance(client, EvadavClient):
                status = client.add_zones_to_list(update.campaign_id, update.zones,
                                                  update.api_key, list_to_add=update.list)

        elif update.action == INCLUDE_ZONE:
            if isinstance(client, PropellerClient):
                status = client.add_zones_to_list(update.campaign_id, update.zones,
                                                  update.api_key, list_type=WHITELIST)
            elif isinstance(client, EvadavClient):
                status = client.add_zones_to_list(update.campaign_id, update.zones,
                                                  update.api_key, list_to_add=update.list)
        else:
            return f"Unknown action: {update.action}"

        return status

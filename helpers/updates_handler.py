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
        pass
    
    def handle(self, update):
        status = None

        try:
            update = Update(**update)
        except ValidationError:
            return f'Incorrect update: {update}'

        if update.ts == PROPELLER_ADS:
            client = PropellerClient()
        elif update.ts == EVADAV:
            client = EvadavClient()
        elif update.ts == MGID:
            client = MGIDClient()
        else:
            return f"Unknown traffic source: {update.ts}"

        if update.action == PLAY_CAMPAIGN:
            status = client.change_campaign_status(update.campaign_id, update.api_key,
                                                   status=PLAY, client_key=update.client_id)
        elif update.action == STOP_CAMPAIGN:
            status = client.change_campaign_status(update.campaign_id, update.api_key,
                                                   status=STOP, client_key=update.client_id)
        elif update.action == EXCLUDE_ZONE or update.action == INCLUDE_ZONE:
            list_ = BLACKLIST if update.action == EXCLUDE_ZONE else WHITELIST

            if isinstance(client, PropellerClient):
                status = client.add_zones_to_list(update.campaign_id, update.zones,
                                                  update.api_key, list_type=list_)
            elif isinstance(client, EvadavClient):
                status = client.add_zones_to_list(update.campaign_id, update.zones,
                                                  update.api_key, list_to_add=update.list)
            elif isinstance(client, MGIDClient):
                status = client.add_zones_to_list(update.campaign_id, update.zones,
                                                  update.api_key, list_type=list_, client_key=update.client_id)
        else:
            return f"Unknown action: {update.action}"

        return status

# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from typing import Optional, List

from pydantic import BaseModel


class Update(BaseModel):
    ts: str  # traffic source, options: Propeller Ads, Evadav, MGID
    action: int  # action code, defined in updates_handler.py
    api_key: str  # API key for traffic source
    campaign_id: str  # campaign id from traffic source
    zones: Optional[List[str]]  # zones list
    list: Optional[str]  # audience (e.g. Evadav)
    client_id: Optional[str]  # client id for mgid

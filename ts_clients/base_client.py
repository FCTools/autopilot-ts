# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>


class TrafficSourceClient:
    def __init__(self):
        pass

    def stop_campaign(self, campaign_id, api_key):
        raise NotImplemented()

    def start_campaign(self, campaign_id, api_key):
        raise NotImplemented()

    def add_zones_to_black_list(self, campaign_id, site_id, api_key):
        raise NotImplemented()

    def add_zones_to_white_list(self, campaign_id, site_id, api_key):
        raise NotImplemented()

"""
Copyright © 2020-2021 FC Tools.
All rights reserved.
Author: German Yakimov
"""


class TrafficSourceClient:
    def __init__(self):
        pass

    def stop_campaign(self, campaign_id, api_key):
        raise NotImplemented()

    def start_campaign(self, campaign_id, api_key):
        raise NotImplemented()

    def add_site_to_black_list(self, site_id, api_key):
        raise NotImplemented()

    def add_site_to_white_list(self, site_id, api_key):
        raise NotImplemented(0)

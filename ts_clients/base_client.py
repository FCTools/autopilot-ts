# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>


class TrafficSourceClient:
    """
    Base class for traffic source clients.
    """

    def __init__(self):
        pass

    def change_campaign_status(self, campaign_id, api_key, status):
        """
        Method for play/stop campaign.

        :param campaign_id: campaign id from traffic source
        :type campaign_id: str
        :param api_key: api key for traffic source
        :type api_key: str
        :param status: campaign status to set: stop/play
        :type status: str

        :return: None
        """

        raise NotImplemented()

    def add_zones_to_list(self, campaign_id, zones_list, api_key, list_type):
        """
        Method for play/stop campaign.

        :param campaign_id: campaign id from traffic source
        :type campaign_id: str
        :param zones_list: list with zones ids
        :type zones_list: list
        :param api_key: api key for traffic source
        :type api_key: str
        :param list_type: type of the list: black/white
        :type list_type: str

        :return: None
        """

        raise NotImplemented()

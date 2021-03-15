# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import os

import redis


class RedisClient:
    """
    Client for redis with basic functionality.
    """

    def __init__(self):
        self._redis_port = os.getenv('REDIS_PORT')
        self._redis_host = os.getenv('REDIS_HOST')

        self._server = redis.Redis(host=self._redis_host, port=self._redis_port)

    @staticmethod
    def _remove_duplicates(dict_):
        res = dict()
        tmp = []

        for key, val in dict_.items():
            if val not in tmp:
                tmp.append(val)
                res[key] = val

        return res

    def get_updates(self):
        """
        Retrieve all updates from redis.

        :return: Dictionary with updates, format: {'task_id': content}
        :rtype: dict
        """

        keys = self._server.keys()
        updates = {}

        if keys:
            for key in keys:
                updates[key] = self._server.get(key)

            self.remove_keys(keys)

        return self._remove_duplicates(updates)

    def append(self, key, value):
        self._server.append(key, value)

    def remove_keys(self, keys):
        self._server.delete(*keys)

    def clear(self):
        self._server.flushdb()

    def close(self):
        self._server.close()

    def __del__(self):
        self.close()

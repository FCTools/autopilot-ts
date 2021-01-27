# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import redis
import os


class RedisClient:
    def __init__(self):
        self._redis_port = os.getenv('REDIS_PORT')
        self._redis_host = os.getenv('REDIS_HOST')

        self._server = redis.Redis(host=self._redis_host, port=self._redis_port)

    def get_updates(self):
        keys = self._server.keys()
        updates = {}

        if keys:
            for key in keys:
                updates[key] = self._server.get(key)

        self.remove_keys(keys)

        return updates

    def append(self, key, value):
        self._server.append(key, value)

    def remove_keys(self, keys):
        self._server.delete(*keys)

    def clear(self):
        self._server.flushdb()

    def __del__(self):
        self._server.close()

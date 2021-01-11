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
        # self._redis_password = os.getenv('REDIS_PASSWORD')

        self._server = redis.Redis(host=self._redis_host, port=self._redis_port)

    def get_updates(self):
        keys = self._server.keys()
        updates = set()

        if keys:
            for key in keys:
                updates.add(self._server.get(key))

            self._server.delete(*keys)

        return updates

    def clear(self):
        self._server.flushdb()

    def __del__(self):
        self._server.close()

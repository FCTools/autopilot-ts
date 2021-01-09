"""
Copyright © 2020-2021 FC Tools.
All rights reserved.
Author: German Yakimov
"""

import json
import redis
import os


class RedisClient:
    def __init__(self):
        self._redis_port = os.getenv('REDIS_PORT')
        self._redis_host = os.getenv('REDIS_HOST')
        self._redis_password = os.getenv('REDIS_PASSWORD')

        self._server = redis.Redis(host=self._redis_host, port=self._redis_port, password=self._redis_password)

    def get_updates(self):
        keys = self._server.keys()
        updates = {}

        for key in keys:
            updates[key] = json.loads(self._server.get(key))

        return updates

    def clear(self):
        self._server.flushdb()

    def __del__(self):
        self._server.close()

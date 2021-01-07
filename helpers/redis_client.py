import redis
import os


class RedisClient:
    def __init__(self):
        self._redis_port = os.getenv('REDIS_PORT')
        self._redis_host = os.getenv('REDIS_HOST')
        self._redis_password = os.getenv('REDIS_PASSWORD')

    def get_updates(self):
        pass

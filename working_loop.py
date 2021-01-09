"""
Copyright © 2020-2021 FC Tools.
All rights reserved.
Author: German Yakimov
"""

import os
import threading
import time

from helpers.redis_client import RedisClient
from helpers.updates_handler import UpdatesHandler

updates_list = {}
lock = threading.Lock()
handler = UpdatesHandler()

# update format:
# {"ts": "prop", "campaign_id": xxxxx, "api_key": xxxxxxx, "action": "start"/"stop"}
#


def process():
    while True:
        with lock:
            if len(updates_list):
                update = updates_list.popitem()
        handler.handle(update)
        time.sleep(5)


DEFAULT_POOL_SIZE = int(os.getenv('POOL_SIZE', 10))
CHECKING_TIMEOUT = float(os.getenv('CHECKING_TIMEOUT', 60))
workers_pool = [threading.Thread(target=process, args=(), daemon=True) for _ in range(DEFAULT_POOL_SIZE)]

redis = RedisClient()

for worker in workers_pool:
    worker.start()

while True:
    with lock:
        updates = redis.get_updates()
    time.sleep(CHECKING_TIMEOUT)

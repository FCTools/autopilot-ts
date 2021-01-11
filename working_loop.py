# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>
import json
import os
import threading
import time

from helpers.redis_client import RedisClient
from helpers.updates_handler import UpdatesHandler

updates_list = set()
lock = threading.Lock()
handler = UpdatesHandler()

# update format:
# {"ts": "prop", "campaign_id": xxxxx, "api_key": xxxxxxx, "action": "start"/"stop"}
#


def process():
    while True:
        with lock:
            update = None
            if len(updates_list):
                update = json.loads(updates_list.pop())

        if update:
            handler.handle(update)
        time.sleep(5)


DEFAULT_POOL_SIZE = int(os.getenv('POOL_SIZE', 10))
CHECKING_TIMEOUT = float(os.getenv('CHECKING_TIMEOUT', 10))
workers_pool = [threading.Thread(target=process, args=(), daemon=True) for _ in range(DEFAULT_POOL_SIZE)]

redis = RedisClient()

for worker in workers_pool:
    worker.start()

while True:
    updates = redis.get_updates()

    with lock:
        updates_list.update(updates)

    time.sleep(CHECKING_TIMEOUT)

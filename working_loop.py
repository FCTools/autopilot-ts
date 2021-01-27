# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import json
import logging
import os
import random
import threading
import time
import platform

from helpers.redis_client import RedisClient
from helpers.updates_handler import UpdatesHandler

updates_list = {}
lock = threading.Lock()
handler = UpdatesHandler()

# update format:
# {"ts": "prop", "campaign_id": xxxxx, "api_key": xxxxxxx, "action": "start"/"stop"}
#

_logger = logging.getLogger(__name__)
redis_client = RedisClient()


def _configure_logger():
    """
    Set logger basic configuration.
    """

    _logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("info_log.log", "w", "utf-8")
    file_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
    )
    file_handler.setLevel(logging.DEBUG)
    _logger.addHandler(file_handler)

    _logger.info(f"Platform: {platform.system().lower()}")
    _logger.info(f"WD: {os.getcwd()}")

    _logger.info("Logger configured.")


def process():
    while True:
        with lock:
            update = None
            if len(updates_list):
                key = random.choice(list(updates_list.keys()))
                update = json.loads(updates_list[key])
                del(updates_list[key])

        if update:
            _logger.info(f'Get new update: {key}')
            status = handler.handle(update)

            if status == 'OK':
                _logger.info(f'Update successfully handled: {key}')
                redis_client.remove_keys([key])
            else:
                _logger.error(f"Can't handle update {key}: {status}")
                time.sleep(10)
                redis_client.append(key, json.dumps(update))

        time.sleep(5)


DEFAULT_POOL_SIZE = int(os.getenv('POOL_SIZE', 5))
CHECKING_TIMEOUT = float(os.getenv('CHECKING_TIMEOUT', 10))

_configure_logger()
workers_pool = [threading.Thread(target=process, args=(), daemon=True) for _ in range(DEFAULT_POOL_SIZE)]

for worker in workers_pool:
    worker.start()

while True:
    updates = redis_client.get_updates()

    with lock:
        updates_list.update(updates)

    time.sleep(CHECKING_TIMEOUT)

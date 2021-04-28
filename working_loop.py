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
import platform
import random
import threading
import time

from helpers.redis_client import RedisClient
from helpers.updates_handler import UpdatesHandler

updates_list = {}
updates_lock = threading.Lock()
redis_lock = threading.Lock()
handler = UpdatesHandler()

# TODO: add handling connection error: redis.exceptions.ConnectionError

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
    """
    Main method, listening for updates in redis and process these updates.

    :return: None
    """

    while True:
        with updates_lock:
            update = None
            if len(updates_list):
                key = random.choice(list(updates_list.keys()))
                try:
                    update = json.loads(updates_list[key])
                except json.JSONDecodeError:
                    _logger.error(f"Can't parse object: {updates_list[key]}")
                del(updates_list[key])

        if update:
            _logger.info(f'Get new update: {key}')
            status = handler.handle(update)

            if status == 'OK':
                _logger.info(f'Update was successfully handled: {key}')

                with redis_lock:
                    redis_client.remove_keys([key])
            else:
                _logger.error(f"Can't handle update {key}: {status}")
                time.sleep(10)

        time.sleep(5)


DEFAULT_POOL_SIZE = int(os.getenv('POOL_SIZE', 5))
CHECKING_TIMEOUT = float(os.getenv('CHECKING_TIMEOUT', 10))

_configure_logger()
workers_pool = [threading.Thread(target=process, args=(), daemon=True) for _ in range(DEFAULT_POOL_SIZE)]

for worker in workers_pool:
    worker.start()

_logger.info('Start workers.')
_logger.info('Start listening for updates...')

try:
    while True:
        with redis_lock:
            updates = redis_client.get_updates()

        if updates:
            _logger.info(f'Get {len(updates)} new updates.')

            with updates_lock:
                updates_list.update(updates)

        time.sleep(CHECKING_TIMEOUT)

except KeyboardInterrupt:
    _logger.info('Catch KeyboardInterrupt. Quit.')
    redis_client.close()
    exit(0)

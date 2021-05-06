# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import os

import psycopg2
from contextlib import closing

from helpers.singleton import Singleton


class Logger(metaclass=Singleton):
    def __init__(self):
        self._user = os.getenv('DB_USER')
        self._password = os.getenv('DB_PASSWORD')
        self._host = os.getenv('DB_HOST')
        self._port = os.getenv('DB_PORT')

    def log_request(self, task_id, request_url, headers, body, type_, response, status_code, description):
        with closing(psycopg2.connect(...)) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM airport LIMIT 5')
                for row in cursor:
                    print(row)


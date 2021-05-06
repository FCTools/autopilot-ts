# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import os
from contextlib import closing

import psycopg2
from psycopg2 import sql


class Logger:
    def __init__(self):
        self._user = os.getenv('DB_USER')
        self._db_name = os.getenv('DB_NAME')
        self._password = os.getenv('DB_PASSWORD')
        self._host = os.getenv('DB_HOST')
        self._port = os.getenv('DB_PORT')

    def log_request(self, task_id, time_, request_url, headers, body, type_, response, status_code, description):
        with closing(psycopg2.connect(dbname=self._db_name, user=self._user,
                                      password=self._password, host=self._host, port=self._port)) as conn:
            with conn.cursor() as cursor:
                conn.autocommit = True
                values = [
                    (task_id, time_, request_url, headers, body, type_, response, status_code, description),
                ]
                insert = sql.SQL('INSERT INTO logs (code, name, country_name) VALUES {}').format(
                    sql.SQL(',').join(map(sql.Literal, values))
                )

                cursor.execute(insert)

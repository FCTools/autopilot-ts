# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-ts.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import os

import psycopg2

conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

cur = conn.cursor()
cur.execute("CREATE TABLE logs (id serial PRIMARY KEY, task_id uuid PRIMARY KEY, "
            "time_ char(32), requests_url char(1024), headers char(2048), body char(16384),"
            "type_ char(10), response char(65536), status_code int, description char(128));")

conn.commit()
conn.close()

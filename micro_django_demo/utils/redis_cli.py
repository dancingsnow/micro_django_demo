#! usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019/7/4
# Author: snow

import os
import redis

conn_pool = redis.ConnectionPool(
    host=os.environ.get('REDIS_HOST', "0.0.0.0"),
    port=6379,
    db=0,
    password=os.environ.get('REDIS_PASS', None),
    decode_responses=True
)

redis_client = redis.Redis(connection_pool=conn_pool)

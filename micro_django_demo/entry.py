#! usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019/7/5
# Author: snow

"""
程序入口
    - 开发，可直接用runserver
    - 生产，用gevent server
"""

import os
from gevent.monkey import patch_all
patch_status = False
if str(os.environ.get("DEBUG")).lower()!='true' or str(os.environ.get("DEBUG_SERVER")).lower()!='true':
    # 跟gevent的多线程有冲突，容易造成死锁的问题
    patch_all(thread=False)
    patch_status = True
from gevent.pywsgi import WSGIServer
from micro_django_demo.wsgi import application
from django.core.management.commands.runserver import Command as DebugServer
import logging


ip = "0.0.0.0"
port = 8000

def product():
    server = WSGIServer((ip, port), application)
    logging.info('Running PRODUCT on http://%s:%d/' % (ip, port))
    server.serve_forever()

def development():
    # server = BaseRunserverCommand()
    server = DebugServer()
    server.handle(use_ipv6=False, addrport="%s:%s"%(ip, port),
                  use_reloader=True, use_threading=True,
                  use_static_handler=True, insecure_serving=True)


if str(os.environ.get("DEBUG")).lower()=='true' and str(os.environ.get("DEBUG_SERVER")).lower()=='true':
    main = development
else:
    main = product


logging.info(">>>>>>>>> RUN MODE: %s , patch_status: %s" %(str(main.__name__), str(patch_status)))


if __name__ == '__main__':
    # main()
    development()


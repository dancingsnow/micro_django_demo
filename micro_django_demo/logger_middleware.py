#! usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019/7/4
# Author: snow

import time
import logging


class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if str(request.path).startswith("/apis"):
            start_time = time.time()
            req_data = ""
            if request.method == 'GET':
                req_data = request.GET.dict()
            elif request.method == 'POST':
                req_data = str(request.body, encoding='utf-8')
            response = self.get_response(request)
            end_time = time.time()
            try:
                log_info = "<<< REQUEST MESSAGE >>>: [req_path]: %s, [mehtod]: %s, [cost_time]: %.2f s, [status]: %s, [req_data]: %s, [resp_data]: %s" % (
                    request.path,
                    request.method,
                    end_time - start_time,
                    response.status_code,
                    req_data,
                    response.data
                )
                logging.info(log_info)
            except AttributeError:
                # AttributeError: 'JsonResponse' object has no attribute 'data'
                logging.warning("JsonResponse/HttpResponse is not recommended, rest-framework.response.Response is GOOD !")
        else:
            response = self.get_response(request)
        return response

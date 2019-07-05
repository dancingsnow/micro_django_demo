#! usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019/7/2
# Author: snow

from django.conf.urls import url
from book_demo.views import test_api, author, author_detail




urlpatterns = [
    url(r"^test/", test_api.TestView.as_view() , name="测试用例"),
    url(r"^test/hello", test_api.TestView.as_view(), name="hello world"),

    url(r"^author/", author.AuthorView.as_view(), name="作者author增删改查"),

    url(r"^author_detail/", author_detail.AuthDetailView.as_view())
]

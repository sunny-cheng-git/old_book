#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sunny"
# Date: 2020-05-21

from django.contrib.auth.middleware import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect
from old_books import settings
import re

class LOGIN_middleware(MiddlewareMixin):
    def process_request(self, request):
        request_url = request.path_info  # 获取请求路径
        if re.search('media',request_url): #media文件不需要认证
            return

        if str(request.user) == 'AnonymousUser':
            if request.path in settings.WHILT_LIST:
                return
            else:
                return redirect('/login/')
        else:
            return



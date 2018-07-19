# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from .settings import USER_AGENT_LIST
import random

class UserAgentMiddleWares(object):
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = user_agent


#
# class ProxiesMiddlerWares(object):
#     def process_request(self, request, spider):
#
#         # 1、免费代理
#         #格式： proxy = "http:ip:port"
#         #2、验证代理
#         #格式：proxy = "http://账户:密码@ip:port"
#
#         #request.meta['proxy'] = proxy
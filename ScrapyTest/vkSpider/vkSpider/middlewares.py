# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random

########################################
#--------DOWNLOADER MIDDLEWARES--------#
########################################
class RandomUserAgent(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self,agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        agent = random.choice(self.agents)
        request.headers.setdefault('User-Agent', agent)
        spider.logger.info('agent: %s' % agent)
        return None

class RandomProxy(object):
    def __init__(self, iplist):  # 初始化一下数据库连接
        self.iplist = iplist

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings.getlist('IPLIST'))

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        proxy = random.choice(self.iplist)
        spider.logger.info('proxy: %s' % proxy)
        request.meta['proxy'] = proxy
        return None

class FixedProxy(object):
    def __init__(self, proxy):  # 初始化一下数据库连接
        self.proxy = proxy

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings.get('PROXY'))

    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = self.proxy
        spider.logger.info('proxy: %s' % self.proxy)
        return None
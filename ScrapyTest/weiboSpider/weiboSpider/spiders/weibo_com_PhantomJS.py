# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector
from scrapy.http import Request, FormRequest
from scrapy.shell import inspect_response
from weiboSpider.items import UserInfoItem, RelationItem
import time

import re



class WeiboComPhantomoJSSpider(CrawlSpider):
    name = 'weibo.com_PhantomJS'
    allowed_domains = ['weibo.com','sina.com.cn']
    start_urls = ['https://weibo.com/p/1005052259181527/info',
                  # 'https://weibo.com/p/1005052259181527/follow',
                  # 'https://weibo.com/p/1005052259181527/follow?relate=fans',
                  ]

    rules = (
        Rule(LinkExtractor(allow=('weibo.com/p/\d+/info',)), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'/follow'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'/info'), callback='parse_item', follow=True),
    )

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'weiboSpider.middlewares.PhantomJSMiddleware': 450,
        }
    }

    phone = '15676371114'
    password = '49e7b513'

    def parse_item(self, response):
        print response
        weibo_item = UserInfoItem()
        try_exist = lambda x: x[0] if x else ''
        # inspect_response(response, self) # 中断并将response传入shell，Ctrl+D退出终端继续
        weibo_item['username'] = try_exist(Selector(response).xpath('//h1[@class="username"]/text()').extract())
        weibo_item['user_id'] = try_exist(Selector(response).re(r"\$CONFIG\['page_id'\]='(\d+)'"))
        weibo_item['follows'] = try_exist(Selector(response).re(u'<strong class="W_f18">(.*)</strong>\s*<span class="S_txt2">关注</span>'))
        weibo_item['followers'] = try_exist(Selector(response).re(u'<strong class="W_f18">(.*)</strong>\s*<span class="S_txt2">粉丝</span>'))
        weibo_item['gender'] = try_exist(Selector(response).re(u'性别：</span>\s*<span class="pt_detail">(.*)</span>'))
        weibo_item['pf_intro'] = try_exist(Selector(response).re(u'简介：</span>\s*<span class="pt_detail">(.*)</span>'))
        weibo_item['pf_birthday'] = try_exist(Selector(response).re(u'生日：</span>\s*<span class="pt_detail">(.*)</span>'))
        weibo_item['pf_loc'] = try_exist(Selector(response).re(u'所在地：</span>\s*<span class="pt_detail">(.*)</span>'))
        weibo_item['pf_email'] = try_exist(Selector(response).re(u'邮箱：</span>\s*<span class="pt_detail">(.*)</span>'))
        weibo_item['pf_regdate'] = try_exist(Selector(response).re(u'注册时间：</span>\s*<span class="pt_detail">(.*)</span>'))

        # self.logger.debug('weibo_item=%s' % weibo_item)
        yield weibo_item

    def start_requests(self):
        # start from here (login)
        login_url = 'https://login.sina.com.cn/signup/signin.php'
        request = Request(login_url,callback=self.after_login,meta={'cookiejar':1}) # 预登陆页面
        request.meta['login'] = True  # True
        yield request  # 最后使用生成器方式提交

    def after_login(self, response):
        # 登陆结束的处理
        uuid = Selector(response).re(r"uid:'(\d+)'")
        if uuid:
            self.logger.info('login success, uuid = %s'%uuid[0])
            request = scrapy.Request(self.start_urls[0], callback=self.parse_item, meta={'cookiejar':response.meta['cookiejar']})  # 预登陆页面
            yield request
        else:
            self.logger.error('login failed')
            return
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



class WeiboComPhantomJSSpider(CrawlSpider):
    name = 'weibo.com_PhantomJS'
    allowed_domains = ['weibo.com','sina.com.cn']
    start_urls = ['https://login.sina.com.cn/signup/signin.php',
                  'https://weibo.com/p/1005052259181527/info',
                  # 'https://weibo.com/p/1005052259181527/follow',
                  # 'https://weibo.com/p/1005052259181527/follow?relate=fans',
                  ]

    rules = (
        # must be tuple
        # 下载allow匹配的链接，继续遍历下一个页面（为什么突然不好用了）
        Rule(LinkExtractor(allow=('weibo.com/p/\d+/info',)), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('weibo.com/p/\d+/follow',)), callback='parse_relation', follow=True),
        # Rule(LinkExtractor(allow=r'/info'), callback='parse_item', follow=True),
    )

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'weiboSpider.middlewares.PhantomJSMiddleware': 450,
        }
    }


    def parse_item(self, response):
        weibo_item = UserInfoItem()
        try_exist = lambda x: x[0] if x else ''
        # inspect_response(response, self) # 中断并将response传入shell，Ctrl+D退出终端继续
        user_id = try_exist(Selector(response).re(r"\$CONFIG\['oid'\]='(\d+)'"))
        weibo_item['username'] = try_exist(Selector(response).xpath('//h1[@class="username"]/text()').extract())
        weibo_item['user_id'] = user_id
        weibo_item['page_id'] = try_exist(Selector(response).re(r"\$CONFIG\['page_id'\]='(\d+)'"))
        weibo_item['followers'] = try_exist(Selector(response).re(u'<strong class="W_f18">(.*)</strong>\s*<span class="S_txt2">关注</span>'))
        weibo_item['followees'] = try_exist(Selector(response).re(u'<strong class="W_f18">(.*)</strong>\s*<span class="S_txt2">粉丝</span>'))
        weibo_item['gender'] = try_exist(Selector(response).re(u'性别：</span>\s*<span class="pt_detail">(.*)</span>'))
        weibo_item['pf_intro'] = try_exist(Selector(response).re(u'简介：</span>\s*<span class="pt_detail">(.*)</span>'))
        weibo_item['pf_birthday'] = try_exist(Selector(response).re(u'生日：</span>\s*<span class="pt_detail">(.*)</span>'))
        weibo_item['pf_loc'] = try_exist(Selector(response).re(u'所在地：</span>\s*<span class="pt_detail">(.*)</span>'))
        weibo_item['pf_email'] = try_exist(Selector(response).re(u'邮箱：</span>\s*<span class="pt_detail">(.*)</span>'))
        weibo_item['pf_regdate'] = try_exist(Selector(response).re(u'注册时间：</span>\s*<span class="pt_detail">(.*)</span>'))

        # self.logger.debug('weibo_item=%s' % weibo_item)
        yield weibo_item

        follower_url = try_exist(Selector(response).xpath('//table[@class="tb_counter"]/tbody/tr/td[1]/a/@href').extract())
        if follower_url:
            follower_request = Request(response.urljoin(follower_url),
                                       meta={'cookiejar':response.meta['cookiejar']},
                                       callback=self.parse_relation)
            follower_request.meta['relation_type'] = 'follower'
            follower_request.meta['user_id'] = user_id
            yield follower_request

        followee_url = try_exist(Selector(response).xpath('//table[@class="tb_counter"]/tbody/tr/td[2]/a/@href').extract())
        if followee_url:
            followee_request = Request(response.urljoin(followee_url),
                                       meta={'cookiejar':response.meta['cookiejar']},
                                       callback=self.parse_relation)
            followee_request.meta['relation_type'] = 'followee'
            followee_request.meta['user_id'] = user_id
            yield followee_request


    def parse_relation(self, response):
        self.logger.debug("crawled url:%s"%response.url)
        # inspect_response(response, self)
        usercards = Selector(response).xpath('//div[@class="info_name W_fb W_f14"]/a[@class="S_txt1"]/@usercard').extract()
        urls = Selector(response).xpath('//div[@class="info_name W_fb W_f14"]/a[@class="S_txt1"]/@href').extract()
        next_page = Selector(response).xpath('//a[@class="page next S_txt1 S_line1"]/@href').extract_first()
        relation_id_pattern = re.compile('id=(\d+)&')

        self.logger.debug("urls=\n%s"%urls)
        for usercard in usercards:
            relation_item = RelationItem()
            relation_item['user_id'] = response.meta['user_id']
            relation_item['relation_type'] = response.meta['relation_type']
            relation_item['relation_id'] = relation_id_pattern.search(usercard).group(1)
            yield relation_item

        if next_page:
            yield Request(response.urljoin(next_page),
                          meta={'cookiejar': response.meta['cookiejar']},
                          callback=self.parse_relation)

        for url in urls:
            yield Request(response.urljoin(url),
                          meta={'cookiejar':response.meta['cookiejar']},
                          callback=self.parse_homepage)

    def parse_homepage(self, response):
        # inspect_response(response, self)
        info_page = Selector(response).xpath('//div[@class="PCD_person_info"]//a[@class="WB_cardmore S_txt1 S_line1 clearfix"]/@href').extract_first()
        if info_page:
            yield Request(response.urljoin(info_page),
                          meta={'cookiejar': response.meta['cookiejar']},
                          callback=self.parse_item)



    def start_requests(self):
        # start from here (login)
        request = Request(self.start_urls[0],callback=self.after_login,meta={'cookiejar':1}) # 预登陆页面
        request.meta['login'] = True  # True
        yield request  # 最后使用生成器方式提交

    def after_login(self, response):
        # 登陆结束的处理
        uuid = Selector(response).re(r"uid:'(\d+)'")
        if uuid:
            self.logger.info('login success, uuid = %s'%uuid[0])
            request = Request(self.start_urls[1], callback=self.parse_item, meta={'cookiejar':response.meta['cookiejar']})  # 预登陆页面
            yield request
        else:
            self.logger.error('login failed')
            return
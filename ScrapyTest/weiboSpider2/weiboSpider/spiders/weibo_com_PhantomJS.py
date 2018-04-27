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
    degree = 1 # 只爬1度联系人

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
        # 解析个人信息
        info_item = UserInfoItem()
        try_exist = lambda x: x[0] if x else ''
        # inspect_response(response, self) # 中断并将response传入shell，Ctrl+D退出终端继续
        user_id = try_exist(Selector(response).re(r"\$CONFIG\['oid'\]='(\d+)'"))
        info_item['username'] = try_exist(Selector(response).xpath('//h1[@class="username"]/text()').extract())
        info_item['user_id'] = user_id
        info_item['page_id'] = try_exist(Selector(response).re(r"\$CONFIG\['page_id'\]='(\d+)'"))
        relation_degree = response.meta['degree']
        info_item['degree'] = relation_degree
        self.logger.info('user_id=%s, username=%s, degree=%s' % (user_id, info_item['username'], relation_degree))
        yield info_item

        # 解析关注人的地址
        relation_degree += 1
        follower_url = try_exist(Selector(response).xpath('//table[@class="tb_counter"]/tbody/tr/td[1]/a/@href').extract())
        if follower_url:
            follower_request = Request(response.urljoin(follower_url),
                                       meta={'cookiejar': response.meta['cookiejar'],
                                             'degree': relation_degree}, # 联系人度数+1
                                       callback=self.parse_relation)
            follower_request.meta['relation_type'] = 'follower'
            follower_request.meta['user_id'] = user_id
            yield follower_request

        followee_url = try_exist(Selector(response).xpath('//table[@class="tb_counter"]/tbody/tr/td[2]/a/@href').extract())
        if followee_url:
            followee_request = Request(response.urljoin(followee_url),
                                       meta={'cookiejar': response.meta['cookiejar'],
                                             'degree': relation_degree},  # 联系人度数+1
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

        # self.logger.debug("urls=\n%s"%urls)
        relation_degree = response.meta['degree']
        user_id = response.meta['user_id']
        relation_type = response.meta['relation_type']
        self.logger.info(response.meta)
        for usercard in usercards:
            relation_item = RelationItem()
            relation_item['user_id'] = user_id
            relation_item['relation_type'] = relation_type
            relation_item['relation_id'] = relation_id_pattern.search(usercard).group(1)
            self.logger.info("user_id=%s, relation_type=%s, relation_id=%s" %
                             (relation_item['user_id'], relation_item['relation_type'], relation_item['relation_id']))
            yield relation_item

        if next_page:
            yield Request(response.urljoin(next_page),
                          meta={'cookiejar': response.meta['cookiejar'],
                                'user_id': user_id,
                                'relation_type': relation_type,
                                'degree': relation_degree},
                          callback=self.parse_relation)

        if relation_degree <= self.degree:
            # 判断关系级别，如果度数超过则不继续爬这些人的信息
            for url in urls:
                yield Request(response.urljoin(url),
                              meta={'cookiejar':response.meta['cookiejar'],
                                    'degree': relation_degree},
                              callback=self.parse_homepage)

    def parse_homepage(self, response):
        # inspect_response(response, self)
        info_page = Selector(response).xpath('//div[@class="PCD_person_info"]//a[@class="WB_cardmore S_txt1 S_line1 clearfix"]/@href').extract_first()
        if info_page:
            yield Request(response.urljoin(info_page),
                          meta={'cookiejar': response.meta['cookiejar'],
                                'degree': response.meta['degree']},
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
            request = Request(self.start_urls[1], callback=self.parse_item,
                              meta={'cookiejar':response.meta['cookiejar'],
                                    'degree':0})  # 预登陆页面
            yield request
        else:
            self.logger.error('login failed')
            return
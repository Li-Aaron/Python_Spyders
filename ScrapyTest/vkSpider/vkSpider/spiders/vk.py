# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request, FormRequest
from scrapy.shell import inspect_response
from scrapy import Selector
from scrapy.http import HtmlResponse
import re

from vkSpider.items import AlbumItem

class VkSpider(CrawlSpider):
    name = 'vk'
    allowed_domains = ['vk.com']

    rules = (
        # Rule(LinkExtractor(allow=r'login'), callback='parse_login', follow=True),
        Rule(LinkExtractor(allow=r'albums'), callback='parse_album', follow=True),
    )
    username = ''
    password = ''

    ########################################
    #-------------ALBUM METHODS------------#
    ########################################
    def parse_album(self, response):
        # 响应Cookie
        Cookie2 = response.headers.getlist('Set-Cookie')
        self.logger.debug('response cookies=\n%s' % Cookie2)
        album_num = response.xpath('//span[@class="ui_crumb_count"]/text()').extract_first()
        album_offsets = range(0,int(album_num),24) # vk 一次动态加载24个album
        for album_offset in album_offsets:
            postdata = {
                'al': '1',
                'al_ad' : '0',
                'offset' : str(album_offset),
                'part' : '1',
            }
            request = FormRequest(response.url,
                                  method='POST',
                                  formdata=postdata,
                                  meta={'cookiejar': response.meta['cookiejar'],
                                        'postdata':postdata},
                                  callback=self.parse_album_full,
                                  dont_filter=True
                                  )
            yield request

    def parse_album_full(self, response):
        # inspect_response(response, self)  # 中断并将response传入shell，Ctrl+D退出终端继续
        # fixme: 这里使用re库是因为response回传是一个注释，如何用Selector解析？
        url_pattern = re.compile(r'<a href="(.*?)"')
        urls = url_pattern.findall(response.text)
        title_pattern = re.compile(r'div class="photos_album_title ge_photos_album" title="(.*?)"')
        titles = title_pattern.findall(response.text)
        album_img_pattern = re.compile(r'style="background-image: url\((.*?)\)')
        album_imgs = album_img_pattern.findall(response.text)
        for url, title, album_img in zip(urls, titles, album_imgs):
            album_item = AlbumItem()
            album_item['url'] = url
            album_item['title'] = title
            album_item['album_img'] = album_img
            yield album_item

    ########################################
    #-------------LOGIN METHODS------------#
    ########################################
    def start_requests(self):
        login_url = 'https://vk.com/login'
        request = Request(login_url, callback=self.parse_login, meta={'cookiejar': 1}, dont_filter=True)  # 预登陆页面
        yield request

    def parse_login(self, response):
        # inspect_response(response, self)  # 中断并将response传入shell，Ctrl+D退出终端继续
        ip_h=response.xpath('//input[@name="ip_h"]/@value').extract_first()
        lg_h=response.xpath('//input[@name="lg_h"]/@value').extract_first()
        postdata = {
            'act': 'login',
            'role': 'al_frame',
            'expire': '',
            'recaptcha': '',
            'captcha_sid': '',
            'captcha_key': '',
            '_origin': 'https://vk.com',
            'ip_h': ip_h,
            'lg_h': lg_h,
            'email': self.username,
            'pass': self.password,
        }
        self.logger.info('postdata=\n%s'%postdata)
        login_url = 'https://login.vk.com/'
        # 响应Cookie
        Cookie2 = response.headers.getlist('Set-Cookie')
        self.logger.debug('response cookies=\n%s' % Cookie2)
        request = FormRequest(login_url,
                              method='POST',
                              formdata=postdata,
                              meta={'cookiejar': response.meta['cookiejar'],
                                    'postdata':postdata},
                              callback=self.after_login,
                              dont_filter=True
                              )
        yield request  # 最后使用生成器方式提交

    def after_login(self, response):
        try_exist = lambda x: x[0] if x else ''
        # inspect_response(response, self)  # 中断并将response传入shell，Ctrl+D退出终端继续
        if Selector(response).re(r"onLoginFailed"):
            self.logger.warning('Login Failed')
            return
        elif Selector(response).re(r"onLoginDone"):
            self.logger.info('Login Success')
            user_id = try_exist(Selector(response).re('/id(\d+)'))
            user_name = try_exist(Selector(response).re("name: '(.*?)'"))
            self.logger.info('user_id=%s, user_name=%s'%(user_id,user_name))
            # 请求Cookie
            Cookie = response.request.headers.getlist('Cookie')
            self.logger.debug('request cookies=\n%s' % Cookie)
            for url in self.start_urls:
                yield Request(url,
                              meta={'cookiejar': True},
                              dont_filter=True,
                              # callback=self.parse_album,
                              )


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CrawlSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider._follow_links = crawler.settings.getbool(
            'CRAWLSPIDER_FOLLOW_LINKS', True)
        spider.username = crawler.settings.get('USERNAME')
        spider.password = crawler.settings.get('PASSWORD')
        spider.start_urls = crawler.settings.getlist('ALBUM_URLS')
        # print spider.username,spider.password
        print spider.start_urls
        return spider

    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                r.meta['cookiejar'] = True # 为了传cookie
                yield rule.process_request(r)
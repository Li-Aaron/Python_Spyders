# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector
from scrapy.http import Request, FormRequest
import time
import rsa
import binascii

from urllib import quote_plus
import base64

# 以下函数取自fuck-login
# Info
# - author : "xchaoinfo"
# - email  : "xchaoinfo@qq.com"
# - date   : "2016.3.7"
def get_su(username):
    """
    对 email 地址和手机号码 先 javascript 中 encodeURIComponent
    对应 Python 3 中的是 urllib.parse.quote_plus
    然后在 base64 加密后decode
    """
    username_quote = quote_plus(username)
    username_base64 = base64.b64encode(username_quote.encode("utf-8"))
    return username_base64.decode("utf-8")

def get_password(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
    message = message.encode("utf-8")
    passwd = rsa.encrypt(message, key)  # 加密
    passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
    return passwd

class WeiboComSpider(CrawlSpider):
    name = 'weibo.com'
    allowed_domains = ['weibo.com','sina.com.cn']
    start_urls = ['https://weibo.com/p/1005052259181527/info?mod=pedit_more']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    phone = '15676371114'
    password = '49e7b513'

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

    def start_requests(self):
        # start from here (login)
        su = get_su(self.phone)
        self.logger.debug('su=%s'%su)
        pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
        pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="
        pre_url = pre_url + str(int(time.time() * 1000))
        request = Request(pre_url,callback=self.start_login,meta={'cookiejar':1}) # 预登陆页面
        request.meta['su'] = su  # 将su用meta方式暂存 [meta:相关页面的元信息]
        yield request  # 最后使用生成器方式提交


    def start_login(self, response):
        # login func
        # 准备数据
        sever_data = eval(response.text.replace("sinaSSOController.preloginCallBack", ''))
        self.logger.debug('sever_data=%s'%sever_data)
        nonce = sever_data['nonce']
        rsakv = sever_data["rsakv"]
        pubkey = sever_data["pubkey"]
        # showpin = sever_data["showpin"] # 先不考虑验证码
        servertime = str(sever_data["servertime"])
        su = response.meta['su']
        sp = get_password(self.password, servertime, nonce, pubkey)

        # 构建post
        postdata = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
            'vsnf': '1',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': sp,
            'sr': '1366*768',
            'encoding': 'UTF-8',
            'prelt': '115',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        self.logger.debug('postdata=%s' % postdata)
        login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        # login_url = 'https://login.sina.com.cn/signup/signin.php'
        self.logger.debug("meta['cookiejar']=%s"%response.meta['cookiejar'])
        request = FormRequest(login_url,
                              method='POST',
                              formdata=postdata,
                              meta={'cookiejar':response.meta['cookiejar']},
                              callback=self.start_login_jump,
                              ) # 预登陆页面
        request.meta['postdata'] = postdata
        yield request  # 最后使用生成器方式提交

    def start_login_jump(self, response):
        # 登陆跳转的处理
        # self.logger.debug('response=%s' % response.text)
        login_jump_url = Selector(response).re(r'location\.replace\([\'"](.*?)[\'"]\)')[0]
        self.logger.debug("login_jump_url=%s" % login_jump_url)
        request = scrapy.Request(login_jump_url, callback=self.after_login, meta={'cookiejar':response.meta['cookiejar']})  # 预登陆页面
        yield request

    def after_login(self, response):
        # 登陆结束的处理
        # self.logger.debug('response=%s' % response.text)
        uuid = Selector(response).re(r'"uniqueid":"(.*?)"')
        if uuid:
            self.logger.info('login success, uuid = %s'%uuid[0])
            request = scrapy.Request(self.start_urls[0], meta={'cookiejar':response.meta['cookiejar']})  # 预登陆页面
            yield request
        else:
            self.logger.error('login failed')
            return
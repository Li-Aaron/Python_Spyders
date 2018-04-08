#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
cnblogs spider using CrawlSpider
@Author: AC
2018-4-7

Xpath:
.       当前节点                    ./system
..      parent节点                  ../system
/       root节点(下一级节点)         /system     system/child
//      任意位置(任意子级节点)        //system     system//child
@        property                   //name[@lang='en'](属性匹配表达式)       //name/a/@herf (选取属性)
*       通配符                     //*[@lang='en']
|       or                        //*[@lang='en'] | //age

LinkExtractor:
allow:              满足表达式的链接提取
deny:               否（优先级高于allow）
allow_domains:
deny_domains:
restrict_xpaths:    提取满足XPath条件的
restrict_css:       提取满足css条件的
tags:               提取指定标记下的链接
attrs:              提取拥有此属性的链接，默认为href
unique:             是否去重
process_value:      值处理函数（优先级高于allow）

Rules:
link_extractor:
callback:           回调函数
follow:             是否需要跟进（默认未定义callback为True，定义callback为False）
process_links:      过滤链接
process_request:    过滤Request
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from cnblogSpider.items import CnblogspiderItem
##############################################
#------------------常量定义------------------#
##############################################

##############################################
#------------------函数定义------------------#
##############################################

##############################################
#------------------类定义--------------------#
##############################################
class CnblogsSpiderCrawl(CrawlSpider):
    name = "cnblogs_crawl" # spider name (unique)
    allowed_domains = ["cnblogs.com"]
    start_urls = [
        "http://www.cnblogs.com/qiyeboy/default.html?page=1"
    ]
    rules = (
        # must be tuple
        # 下载allow匹配的链接，继续遍历下一个页面
        Rule(LinkExtractor(allow=("/qiyeboy/default.html\?page=\d{1,}",)),
             follow=True,
             callback='parse_item'
        ),
    )

    def parse_item(self, response):
        '''
        实现response的解析
        解析目录
        '''
        papers = response.xpath(".//*[@class='day']")
        # test
        # from scrapy.shell import inspect_response
        # inspect_response(response, self) # 中断并将response传入shell，Ctrl+D退出终端继续

        for paper in papers:
            # extract data
            url = paper.xpath(".//*[@class='postTitle']/a/@href").extract()[0]
            title = paper.xpath(".//*[@class='postTitle']/a/text()").extract()[0]
            time = paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content = paper.xpath(".//*[@class='postCon']//text()").extract()[0].replace(u'\xa0', u' ') # 去&nbsp;(\xa0) 不然windows下gbk打不出来(utf-8)可以
            item = CnblogspiderItem(url=url, title=title, time=time, content=content)
            request = scrapy.Request(url=url, callback=self.parse_body) # 解析正文
            request.meta['item'] = item # 将item用meta方式暂存 [meta:相关页面的元信息]
            yield request # 最后使用生成器方式提交


    def parse_body(self, response):
        '''解析正文'''
        item = response.meta['item']
        body = response.xpath(".//*[@class='postBody']")
        item['image_urls'] = body.xpath('.//img//@src').extract()
        yield item # 最后使用生成器方式提交


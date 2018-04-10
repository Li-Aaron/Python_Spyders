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
from scrapy.spiders import XMLFeedSpider
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
class CnblogsSpiderXML(XMLFeedSpider):
    name = "cnblogs_xml" # spider name (unique)
    allowed_domains = ["cnblogs.com"]
    start_urls = [
        "http://feed.cnblogs.com/blog/u/269038/rss"
    ]
    iterator = 'html' # default
    itertag = 'entry'

    def adapt_response(self, response):
        '''return a altered response'''
        return response

    def parse_node(self, response, selector):
        print selector.xpath('id/text()').extract()[0]
        print selector.xpath('title/text()').extract()[0]
        print selector.xpath('summary/text()').extract()[0].replace(u'\xa0', u' ')


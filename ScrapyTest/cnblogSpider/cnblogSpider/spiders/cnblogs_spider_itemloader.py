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
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity, MapCompose, Join

from cnblogSpider.items import CnblogspiderItem, newCnblogItem
##############################################
#------------------常量定义------------------#
##############################################

##############################################
#------------------函数定义------------------#
##############################################

##############################################
#------------------类定义--------------------#
##############################################
class CnblogsSpiderItemloader(CrawlSpider):
    name = "cnblogs_itemloader" # spider name (unique)
    custom_settings = {
        'ITEM_PIPELINES': {
            'cnblogSpider.pipelines.CnblogMongoPipeline': 100,
        }
    }
    allowed_domains = ["cnblogs.com"]
    start_urls = [
        "http://www.cnblogs.com/qiyeboy/default.html?page=1"
    ]
    rules = (
        # must be tuple
        # 下载allow匹配的链接，继续遍历下一个页面
        Rule(LinkExtractor(allow=("/qiyeboy/default.html\?page=\d{1,}",)),
             follow=True,
             callback='parse_item_loader'
        ),
    )


    def parse_item_loader(self, response):
        '''item loader 模式'''
        item = self._parse_item_loader(response)
        print item['title']
        print item['time']
        yield item # 最后使用生成器方式提交

    def _parse_item_loader(self, response):
        l = CnblogLoader2(item=newCnblogItem(), response=response)
        # xpath 方式提取（收集），一个字段可以用多个收集
        l.add_xpath('url', ".//*[@class='postTitle']/a/@href")
        l.add_xpath('title', ".//*[@class='postTitle']/a/text()")
        l.add_xpath('time', ".//*[@class='dayTitle']/a/text()")
        l.add_xpath('content', ".//*[@class='postCon']//text()")
        return l.load_item()



class CnblogLoader(ItemLoader):
    # 优先级最低 默认输入输出处理器
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    # 优先级最高 输入_in 输出_out
    title_in = MapCompose(unicode.title) # unicode 逐单词首字母大写
    title_out = Join() # 逐元素迭代插入separator=' '

class CnblogLoader2(CnblogLoader):
    '''重构可以直接修改父类的内容'''

    # MapCompose和Compose的区别：
    # MapCompose —— 整体迭代通过function1 再整体迭代通过function2
    # Compose —— 逐元素通过function1 再通过function2 再组成迭代器
    title_in = MapCompose(lambda x:x.replace(u'-',u'[-]'), CnblogLoader.title_in) # 串联




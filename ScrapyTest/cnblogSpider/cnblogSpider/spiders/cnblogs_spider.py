#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
cnblogs spider
@Author: AC
2018-4-3

Xpath:
.       当前节点                    ./system
..      parent节点                  ../system
/       root节点(下一级节点)         /system     system/child
//      任意位置(任意子级节点)        //system     system//child
@       property                   //name[@lang='en'](属性匹配表达式)       //name/a/@herf (选取属性)
*       通配符                     //*[@lang='en']
|       or                        //*[@lang='en'] | //age

'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import scrapy
from scrapy import Selector

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
class CnblogsSpider(scrapy.Spider):
    name = "cnblogs" # spider name (unique)
    allowed_domains = ["cnblogs.com"]
    start_urls = [
        "https://www.cnblogs.com/qiyeboy"
    ]

    def parse(self, response):
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
            content = paper.xpath(".//*[@class='postCon']//text()").extract()[0]
            print url,title,time,content.replace(u'\xa0', u' ') # 去&nbsp;(\xa0) 不然windows下gbk打不出来(utf-8)可以
            item = CnblogspiderItem(url=url, title=title, time=time, content=content)
            request = scrapy.Request(url=url, callback=self.parse_body) # 解析正文
            request.meta['item'] = item # 将item用meta方式暂存 [meta:相关页面的元信息]
            yield request # 最后使用生成器方式提交
        # \s        匹配任何不可见字符，包括空格、制表符、换页符等等。等价于[ \f\n\r\t\v]。
        # \S        匹配任何可见字符。等价于[ ^ \f\n\r\t\v]。
        next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>') # 这里不要提取，如果没有元素会报错
        if next_page:
            yield scrapy.Request(url=next_page[0], callback=self.parse) # 链接与回调方法 callback指定由谁响应此url


    def parse_body(self, response):
        '''解析正文'''
        item = response.meta['item']
        body = response.xpath(".//*[@class='postBody']")
        item['image_urls'] = body.xpath('.//img//@src').extract()
        yield item # 最后使用生成器方式提交


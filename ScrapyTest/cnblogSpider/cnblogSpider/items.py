# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnblogspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 用这个class创建的item用法类似于dict，但不是dict(只能建立已经有的值)
    # 但是可以和dict转化
    url = scrapy.Field() # dict的子类 class Field(dict)
    time = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    # files = scrapy.Field()
    # file_urls = scrapy.Field()

class newCnblogItem(CnblogspiderItem):
    body = scrapy.Field()
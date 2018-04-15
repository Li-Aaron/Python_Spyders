# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Identity, MapCompose, Join
from w3lib.html import remove_tags

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
    time = scrapy.Field(
        # 优先级高于default_input_processor
        # 优先级低于field_in field_out字段
        input_processor = MapCompose(lambda x:u'时间：'+x),
        output_processor = TakeFirst(),
    )
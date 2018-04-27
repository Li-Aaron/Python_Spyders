# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # 用户基本信息
    user_id = scrapy.Field()        # ID
    page_id = scrapy.Field()        # page ID
    username = scrapy.Field()       # 昵称
    degree = scrapy.Field()         # 度

class RelationItem(scrapy.Item):
    # define the fields for your item here like:
    # 用户相关的用户
    user_id = scrapy.Field()        # ID
    relation_type = scrapy.Field()  # relation类型(follower,followee)
    relation_id = scrapy.Field()    # 与我有关系的id列表

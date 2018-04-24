# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserInfoItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()        # ID
    username = scrapy.Field()       # 昵称
    gender = scrapy.Field()         # 性别
    pf_intro = scrapy.Field()       # 简介
    pf_birthday = scrapy.Field()    # 生日
    pf_loc = scrapy.Field()         # 所在地
    pf_email = scrapy.Field()       # 邮箱
    pf_regdate = scrapy.Field()     # 注册时间
    follows = scrapy.Field()        # 关注数
    followers = scrapy.Field()      # 粉丝数

class RelationItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()        # ID
    relation_type = scrapy.Field()  # relation类型
    relation_id = scrapy.Field()    # 与我有关系的id列表
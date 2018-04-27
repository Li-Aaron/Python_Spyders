# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import scrapy
from scrapy.exceptions import DropItem
from weiboSpider.items import *

########################################
#----------MONGO DB PIPELINES----------#
########################################
class MongoItemPipeline(object):
    '''尝试open_spider, close_spider, from_crawler三个方法'''

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # classmethod 可以不用实例化 直接用类方法调用
    @classmethod
    def from_crawler(cls, crawler):
        # 返回自身 生成实例
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE','items'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        '''核心'''
        user_id = item['user_id']
        if user_id:
            if isinstance(item, UserInfoItem):
                self._process_info_item(item, spider)
            elif isinstance(item, RelationItem):
                self._process_relation_item(item, spider)
            return item
        else:
            raise DropItem("Missing user_id in %s" % item)

    def _process_info_item(self, item, spider):
        # 需要查重/更新
        collection = self.db['UserInfo']
        item_find = collection.find({'user_id':item['user_id']})
        if item_find.count():
            if item != item_find[0]:
                collection.update({'user_id':item['user_id']},{'$set':item})
                spider.logger.info('Updated user_id: %s'%item['user_id'])
            else:
                spider.logger.warning('Duplicated user_id: %s' % item['user_id'])
        else:
            collection.insert(dict(item))


    def _process_relation_item(self, item, spider):
        # 需要查重、不更新
        collection = self.db['Relation']
        item_find = collection.find_one(item)
        if not item_find:
            collection.insert(dict(item))
        else:
            spider.logger.warning('Duplicated Relation: \n%s' % item)
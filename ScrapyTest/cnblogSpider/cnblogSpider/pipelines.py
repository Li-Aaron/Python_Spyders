# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json,os
import pymongo
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class CnblogspiderPipeline(object):
    '''需要先注册到settings.py中的ITEM_PIPELINES变量中'''
    def __init__(self):
        self.filename = 'paper.json'
        self._init_file()

    def _init_file(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)


    def process_item(self, item, spider):
        if item['title']:
            self.write_file_as_json(item)
            return item
        else:
            raise DropItem("Missing title in %s" % item)


    def write_file(self, content):
        with open(self.filename, 'ab') as f:
            f.write(content)

    def write_file_as_json(self, content):
        content_line = json.dumps(dict(content)) + '\n'
        self.write_file(content_line)

class CnblogMongoPipeline(object):
    '''尝试open_spider, close_spider, from_crawler三个方法'''
    collection_name = 'scrapy_items'
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
        item_title = item['title']
        if item_title:
            collection = self.db[self.collection_name]
            item_find = collection.find({'title': item_title})
            if item_find.count():
                # print 'found'
                if item != item_find[0]:
                    # print 'same'
                    collection.update({'title': item_title}, {'$set': item})
            else:
                # print 'not found'
                collection.insert(dict(item))
            return item
        else:
            raise DropItem("Missing title in %s" % item)


class CnblogspiderImagesPipeline(ImagesPipeline):
    '''定制ImagesPipeline(暂时用不到)'''
    def get_media_requests(self, item, info):
        for image_url in item.get(self.images_urls_field):
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no images')
        item['image_paths'] = image_paths
        return item

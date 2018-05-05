# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# from scrapy.http import Request
from scrapy.exceptions import DropItem
from vkSpider.items import *
from scrapy.pipelines.images import ImagesPipeline


class VkSpiderPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

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
        user_id = item['id']
        if user_id:
            if isinstance(item, AlbumItem):
                self._process_album_item(item, spider)
            elif isinstance(item, PhotoItem):
                self._process_photo_item(item, spider)
            return item
        else:
            raise DropItem("Missing id in %s" % item)

    def _process_album_item(self, item, spider):
        # 需要查重/更新
        collection = self.db.Album
        item_find = collection.find({'id':item['id']})
        if item_find.count():
            if item != item_find[0]:
                collection.update({'id':item['id']},{'$set':item})
                spider.logger.info('[ALBUM] Updated id: %s, title: %s'%(item['id'], item['title']))
            else:
                spider.logger.debug('[ALBUM] Duplicated id: %s, title: %s'%(item['id'], item['title']))
        else:
            collection.insert(dict(item))
            spider.logger.info('[ALBUM] Crawled id: %s, title: %s' % (item['id'], item['title']))


    def _process_photo_item(self, item, spider):
        # 需要查重、不更新
        collection = self.db.Photo
        item_find = collection.find_one(item)
        if not item_find:
            collection.insert(dict(item))
            spider.logger.info('[PHOTO] Crawled album_title: %s, id: %s' % (item['album_title'], item['id']))
        else:
            spider.logger.debug('[PHOTO] Duplicated album_title: %s, id: %s' % (item['album_title'], item['id']))



class VkImagesPipeline(ImagesPipeline):
    '''定制ImagesPipeline'''

    def get_media_requests(self, item, info):
        if isinstance(item, PhotoItem):
            image_url = item.get(self.images_urls_field)
            request = scrapy.Request(image_url)
            request.meta['user_id'] = item['user_id']
            request.meta['album_title'] = item['album_title']
            request.meta['image_id'] = item['id']
            yield request
        elif isinstance(item, AlbumItem):
            image_url = item.get(self.images_urls_field)
            request = scrapy.Request(image_url)
            request.meta['user_id'] = item['user_id']
            request.meta['album_title'] = item['title']
            request.meta['image_id'] = item['id']
            yield request


    def file_path(self, request, response=None, info=None):
        '''自定义文件名'''
        user_id = request.meta['user_id']
        album_title = request.meta['album_title']
        image_id = request.meta['image_id']

        return '%s/%s/%s.jpg' % (user_id, album_title, image_id)

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json,os
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

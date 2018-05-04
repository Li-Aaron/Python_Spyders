# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AlbumItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()        # album url
    title = scrapy.Field()      # album title
    id = scrapy.Field()         # album id
    user_id = scrapy.Field()

    image_url = scrapy.Field()  # photo url
    images = scrapy.Field()     # photo result


class PhotoItem(scrapy.Item):
    id = scrapy.Field()                 # photo id
    album_id = scrapy.Field()
    user_id = scrapy.Field()
    album_title = scrapy.Field()
    image_url = scrapy.Field()          # photo url
    images = scrapy.Field()             # photo result
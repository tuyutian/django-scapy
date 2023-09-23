# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ContentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    tag = scrapy.Field()
    create_time = scrapy.Field()
    thumb = scrapy.Field()
    origin_url = scrapy.Field()
    cate_id = scrapy.Field()
    image_urls = scrapy.Field()
    pass


class ThumbItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()

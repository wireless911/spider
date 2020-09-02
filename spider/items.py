# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    address = scrapy.Field()
    industry = scrapy.Field()
    product_name = scrapy.Field()
    product_address = scrapy.Field()
    total_area = scrapy.Field()
    rental_area = scrapy.Field()
    layer_height = scrapy.Field()
    property = scrapy.Field()
    power = scrapy.Field()
    tranffic = scrapy.Field()
    status = scrapy.Field()
    status2 = scrapy.Field()
    mobile = scrapy.Field()
    email = scrapy.Field()
    user = scrapy.Field()
    intro = scrapy.Field()


    pass

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThrdmoduleItem(scrapy.Item):
    url = scrapy.Field()
    f_n = scrapy.Field()

class SpbuItem(scrapy.Item):
    url = scrapy.Field()
    f_n = scrapy.Field()
    
class TgrItem(scrapy.Item):
    url = scrapy.Field()
    f_n = scrapy.Field()

class MsuItem(scrapy.Item):
    url = scrapy.Field()
    f_n = scrapy.Field()

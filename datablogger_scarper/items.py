# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DatabloggerScarperItem(scrapy.Item):
    record_type = scrapy.Field()
    url_from = scrapy.Field()
    url_to = scrapy.Field()
    url_status = scrapy.Field()

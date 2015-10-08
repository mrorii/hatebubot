# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class HatebuEntry(Item):
    title = Field()
    url = Field()
    tags = Field()
    category = Field()
    num_users = Field()
    create_date = Field()

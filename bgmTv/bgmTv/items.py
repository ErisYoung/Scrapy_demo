# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from  scrapy import Field


class BgmtvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=Field()
    title_jap=Field()
    episodes=Field()
    date=Field()
    staffs=Field()
    score=Field()
    score_num=Field()
    image_name=Field()
    image_url=Field()
    rank=Field()

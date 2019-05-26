# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class QuotesPipeline(object):
    def process_item(self, item, spider):
        return item

class TextPipeline():
    def __init__(self):
        self.init=50

    def process_item(self,item,spider):
        if item['text']:
            if len(item['text'])>self.init:
                item['text']=item['text'][0:self.init]+'...'
                return item
        else:
            return DropItem(item)


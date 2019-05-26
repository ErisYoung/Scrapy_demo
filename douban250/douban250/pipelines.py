# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from douban250.settings import mongo_db,mongo_table,mongo_url
from scrapy.pipelines.images import ImagesPipeline
import scrapy
# 开启settings 里的设置
class Douban250Pipeline(object):
    def __init__(self):
        url=mongo_url
        dbname=mongo_db
        dbtable=mongo_table
        client=pymongo.MongoClient(url)
        db=client[dbname]
        self.port=db[dbtable]
    # item 为从parse yeild 过来的数据
    def process_item(self, item, spider):
        data=dict(item)
        self.port.insert(data)
        return item


class Douban250ImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        url = item['imageurl']
        yield scrapy.Request(url)
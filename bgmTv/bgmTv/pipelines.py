# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

import scrapy
from scrapy.pipelines.images import ImagesPipeline


class ImagesDownPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_url']:
            yield scrapy.Request(image_url, meta={"name": item['title']})

    def file_path(self, request, response=None, info=None):
        filename = "{}.jpg".format(request.meta['name'])
        return filename


class BgmtvPipeline(object):
    collection = "bgmAnimateRank"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        table = self.db[self.collection]
        table.drop()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB")
        )

    def close(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        table = self.db[self.collection]
        table.insert_one(dict(item))

        return item


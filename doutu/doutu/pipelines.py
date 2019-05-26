# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import re


class ImagesrenamePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_url']:
            # 使用request传到file_path
            print(image_url+"---------------")
            yield Request(image_url, meta={'name': item['image_name']})

    def file_path(self, request, response=None, info=None):
        name_ = request.meta['name']
        name = re.sub(r'[？\\*|“<>:/]', '', name)
        image_guid = request.url.split('/')[-1]
        filename = u'{0}/{1}'.format(name, image_guid)
        return filename

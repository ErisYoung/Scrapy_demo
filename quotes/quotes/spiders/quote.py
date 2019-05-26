# -*- coding: utf-8 -*-
import scrapy
from lxml import etree


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/get']

    def parse(self, response):
        self.logger.debug(response.text)
        self.logger.debug("Status Code: "+str(response.status))



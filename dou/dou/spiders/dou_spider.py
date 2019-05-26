# -*- coding: utf-8 -*-
import scrapy
from lxml import etree


class DouSpiderSpider(scrapy.Spider):
    name = 'dou_spider'
    allowed_domains = ['https://movie.douban.com/']
    start_urls = ['https://movie.douban.com/']

    def parse(self, response):
        # print(text)
        print(response.text)
        print(response.xpath("//div[@class='billboard-bd']//tr/text()").extract())
        # print(response.xpath(".//button[@type='submit']/text()"))
        yield scrapy.Request("https://movie.douban.com/",callback=self.parse)

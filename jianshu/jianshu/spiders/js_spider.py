# -*- coding: utf-8 -*-
import scrapy
from jianshu.items import JianshuItem
from lxml import etree
import re


class JsSpiderSpider(scrapy.Spider):
    name = 'js_spider'
    init_following_url = 'http://www.jianshu.com/users/3aa040bf0610/following'

    def start_requests(self):
        yield scrapy.Request(url=self.init_following_url, callback=self.parse)

    def parse(self, response):
        selector = etree.HTML(response.text)

        item = JianshuItem()
        id = selector.xpath('//div[@class="main-top"]/div[@class="title"]/a/@href')[0]
        item['id'] = re.search('/u/(.*)', id).group(1)
        item['name'] = selector.xpath('//div[@class="main-top"]/div[@class="title"]/a/text()')[0]
        item['followings'] = selector.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li[1]//p/text()')[0]
        item['followers'] = selector.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li[2]//p/text()')[0]
        item['articles'] = selector.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li[3]//p/text()')[0]
        item['words'] = selector.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li[4]//p/text()')[0]
        item['likes'] = selector.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li[5]//p/text()')[0]
        yield item

        page_all = selector.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li[1]//p/text()')[0]
        page_all = int(page_all)
        if page_all % 9 == 0:
            page_num = int(page_all / 9)
        else:
            page_num = int(page_all / 9) + 1

        for i in range(1, page_num):
            url = response.url + '?page={}'.format(str(i))
            yield scrapy.Request(url=url, callback=self.parse_infor)

    def parse_infor(self, response):
        sel = etree.HTML(response.text)

        id_lists = sel.xpath('//div[@class="info"]/a/@href')
        for id in id_lists:
            id = re.search(r'/u/(.*)', id).group(1)
            url = 'http://www.jianshu.com/users/{}/following'.format(id)
            yield scrapy.Request(url=url, callback=self.parse)

# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from comment.items import CommentItem
from lxml import etree


class CommentSpiderSpider(scrapy.Spider):
    name = 'comment_spider'
    allowed_domains = ['https://movie.douban.com/subject/25823277']

    def start_requests(self):
        tempurl = 'https://movie.douban.com/subject/25823277/comments?start={}&limit=20&sort=new_score&status=P'
        page = 3201
        for i in range(page):
            url = tempurl.format(str(i * 20))
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = etree.HTML(response.text)
        item = CommentItem()

        item['comments'] = selector.xpath('//div[@class="comment"]/p/span/text()')
        print(item['comments'])
        yield item

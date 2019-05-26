# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from doutu.items import DoutuItem

class DoutulaSpider(CrawlSpider):
    name = 'doutula'
    allowed_domains = ['www.doutula.com']
    start_urls = ['http://www.doutula.com']

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # 对于入口的url 的页面 的url 进行规则匹配
        # follow 为True 则一直回调和响应，在匹配的url 中，再次匹配

        # Rule(LinkExtractor(allow=r'http://www.doutula.com/article/detail/\d+')),
        Rule(LinkExtractor(allow=r'http://www.doutula.com/article/detail/\d+'), callback='parse_item', follow=False),

    )

    def parse_item(self, response):
        i=DoutuItem()
        # 图片管道字典设置，
        i['image_url']=response.xpath(".//div[@class='pic-content']//img/@src").extract()
        i['image_name']=response.xpath(".//div[@class='pic-title']//a/text()").extract()
        print(i)
        # print(i['image_urls'])
        # print(i['images'])
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        # yield i

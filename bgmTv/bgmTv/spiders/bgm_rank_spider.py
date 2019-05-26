# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from bgmTv.items import BgmtvItem
import re


class BgmRankSpiderSpider(scrapy.Spider):
    name = 'bgm_rank_spider'
    url = 'https://bgm.tv/anime/browser?sort=rank&page={}'
    page_num = 10


    def start_requests(self):
        for i in range(self.page_num):
            url = self.url.format(str(i + 1))
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        seletor = etree.HTML(response.text)
        ul = seletor.xpath("//div[@class='section']//ul//li")
        for i in ul:
            item = BgmtvItem()
            item['title'] = i.xpath(".//div//a/text()")[0]
            title_jap= i.xpath(".//div//h3//Small/text()")
            if len(title_jap)!=0:
                item['title_jap']=title_jap[0]
            else:
                item['title_jap']="无"

            infor = i.xpath(".//div//p[@class='info tip']/text()")[0].split(" / ")
            item['episodes'] = re.search(r'\d+', infor[0]).group(0)

            if len(infor) >=3:
                item['staffs'] = ",".join(infor[2:])
                item['date'] = infor[1]
            elif len(infor) ==2:
                item['date'] = infor[1]
                item['staffs']="无"
            else:
                item['date'] = "无"
                item['staffs'] = "无"

            item['score'] = i.xpath(".//div//p[@class='rateInfo']//Small/text()")[0]
            num = i.xpath(".//div//p[@class='rateInfo']//span[2]/text()")[0]
            item['score_num'] = re.search(r'\d+', num).group(0)

            url_str = i.xpath(".//img[@class='cover']/@src")[0]
            item['image_name'] = url_str.split("/")[-1]
            item['image_url'] = ["https:" + url_str]

            item['rank'] = i.xpath(".//div//span[1]/text()")[0]

            # print(item)
            yield item

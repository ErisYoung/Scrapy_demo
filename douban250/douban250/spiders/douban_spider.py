# -*- coding: utf-8 -*-
import scrapy
from douban250.items import Douban250Item

# scrapy startproject 【name】
# 在 spiders 文件夹中 scrapy genspider 【name】 【domain】 生成该.py
#  scrapy crawl douban_spider 执行
# scrapy crawl douban_spider -o test.json/csv
class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名称，不与项目名重复
    name = 'douban_spider'
    # 允许的域名，只抓取其下的
    allowed_domains = ['movie.douban.com']
    # 入口url
    start_urls = ['https://movie.douban.com/top250']

    #解析从下载器返回的res
    def parse(self, response):
        print(response.request.headers['User-Agent'])
        # print(response.request.meta['proxy'])
        movie_list=response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i in movie_list:
            douban_item=Douban250Item()
            douban_item['imageurl']=""
            # extract 返回一个结果列表
            douban_item['serial_number']=i.xpath(".//div[@class='item']//em/text()").extract_first() # 解析第一个数据
            douban_item['movie_name']=i.xpath(".//div[@class='info']//div[@class='hd']/a/span[1]/text()").extract_first()
            content=i.xpath(".//div[@class='info']//div[@class='bd']//p[1]/text()").extract()
            # 被分为多端，对于每端
            contents=""
            for i_content in content:
                contents+="".join(i_content.split())
            douban_item['introduce']=contents
            # print(contents)
            douban_item['star']=i.xpath(".//div[@class='info']//div[@class='bd']//div[@class='star']//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate']=i.xpath(".//div[@class='info']//div[@class='bd']//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describle']=i.xpath(".//div[@class='info']//div[@class='bd']//p[@class='quote']//span/text()").extract_first()
            # 将数据yeild 到管道
            yield douban_item

        next_link=response.xpath("//span[@class='next']//link/@href").extract()
        # print(next_link)
        if next_link:
            next_link=next_link[0]
            # 翻页，回调函数
            yield scrapy.Request("https://movie.douban.com/top250"+next_link,callback=self.parse)

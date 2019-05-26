# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver


class JdSpiderSpider(scrapy.Spider):
    name = 'jd_spider'

    def __init__(self):
        SERVICE_ARGS = [ '--disk-cache=true', '--ignore-ssl-errors=true']
        self.browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
        self.browser.set_page_load_timeout(30)
        self.browser.set_window_size(1400, 900)

    def closed(self, spider):
        print("closed")
        self.browser.close()

    def start_requests(self):
        start_urls = [
            'https://search.jd.com/Search?keyword=%E6%96%87%E8%83%B8&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&page={}&s=1&click=0'.format(
                str(i)) for i in range(1, 2, 2)]
        for url in start_urls:
            print(url+" ----------------")
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = response.xpath('//ul[@class="gl-warp clearfix"]/li')
        print('---------------------------------------------------')
        print(len(selector))
        print('---------------------------------------------------')

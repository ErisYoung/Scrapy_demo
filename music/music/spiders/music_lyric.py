# -*- coding: utf-8 -*-
import scrapy
from music.items import MusicItem
from urllib.parse import quote
from lxml import etree
from scrapy import Request


class MusicLyricSpider(scrapy.Spider):
    name = 'music_lyric'

    def start_requests(self):
        singer = "周杰伦"
        url = 'http://www.xiami.com/search/song/page/{}?spm=a1z1s.3521869.0.0.Nv2jr2&key={}&category=-1'

        for i in range(5):
            url = url.format(str(i + 1), quote(singer))
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("----------------------------1")
        selector = etree.HTML(response.text)
        hrefs = selector.xpath('//td[@class="song_name"]/a[1]/@href')
        titles = selector.xpath('//td[@class="song_name"]/a[1]/@title')
        for href, title in zip(hrefs, titles):
            yield scrapy.Request(url="http://"+href, callback=self.parse_content, meta={'title': title})
            break

    def parse_content(self, response):
        print("----------------------------2")
        selector = etree.HTML(response.text)

        song_list = selector.xpath('//div[@class="lrc_main"]/text()')

        song = []

        for line in song_list:
            song.append(line.strip())

        result = ', '.join(song)

        item = MusicItem()
        item['title'] = response.meta['title']
        item['song'] = result
        print(item)
        yield item

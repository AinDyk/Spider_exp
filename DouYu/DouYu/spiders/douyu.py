# -*- coding: utf-8 -*-
import scrapy
import json
from DouYu.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['capi.douyucdn.cn']
    offset = 0
    url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="
    start_urls = [url+str(offset)]

    def parse(self, response):
        data_list = json.loads(response.body)['data']

        if data_list:
            for data in data_list:
                item = DouyuItem()
                item['room_id'] = data['room_id']
                item['image_src'] = data['vertical_src']
                item['nick_name'] = data['nickname']
                item['anchor_city'] = data['anchor_city']

                yield item

                self.offset +=20
                yield scrapy.Request(url=self.url+str(self.offset),callback=self.parse)

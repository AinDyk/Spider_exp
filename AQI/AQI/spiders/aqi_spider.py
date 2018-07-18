# -*- coding: utf-8 -*-
import scrapy
from ..items import AqiItem

class AqiSpiderSpider(scrapy.Spider):
    name = 'aqi_spider'
    allowed_domains = ['aqistudy.cn']
    base_url = "https://www.aqistudy.cn/historydata/"
    start_urls = [base_url]

    def parse(self, response):
        link_list = response.xpath("//div[@class='bottom']/ul/div[2]/li/a/@href").extract()
        name_list = response.xpath("//div[@class='bottom']/ul/div[2]/li/a/text()").extract()

        for link,name in zip(link_list[10:11],name_list[10:11]):
            yield scrapy.Request(self.base_url+link,callback=self.parse_month,meta={"name":name})

    def parse_month(self,response):
        link_list = response.xpath("//ul[@class='unstyled1']/li/a/@href").extract()
        for link in link_list[1:4]:
            yield scrapy.Request(self.base_url+link,callback=self.parse_day,meta=response.meta)

    def parse_day(self,response):
        tr_list = response.xpath("//div[@class='row']//tr")
        tr_list.pop(0)
        for tr in tr_list:
            item = AqiItem()
            item['city'] = response.meta['name']
            item['date'] = tr.xpath('./td[1]/text()').extract_first()
            item['aqi'] = tr.xpath('./td[2]/text()').extract_first()
            item['level'] = tr.xpath('./td[3]/span/text()').extract_first()
            item['pm2_5'] = tr.xpath('./td[4]/text()').extract_first()
            item['pm10'] = tr.xpath('./td[5]/text()').extract_first()
            item['so2'] = tr.xpath('./td[6]/text()').extract_first()
            item['co'] = tr.xpath('./td[7]/text()').extract_first()
            item['no2'] = tr.xpath('./td[8]/text()').extract_first()
            item['o3'] = tr.xpath('./td[9]/text()').extract_first()
            yield item

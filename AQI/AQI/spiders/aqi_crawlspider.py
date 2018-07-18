# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import AqiItem
import urllib


class AqiCrawlspiderSpider(CrawlSpider):
    name = 'aqi_crawlspider'
    allowed_domains = ['aqistudy.cn']
    start_urls = ["https://www.aqistudy.cn/historydata/"]

    rules = (
        Rule(LinkExtractor(allow=r'monthdata\.php\?city='), follow=True),
        Rule(LinkExtractor(allow=r'daydata\.php\?city='), callback='parse_day', follow=False),
    )

    def parse_day(self,response):
        url = response.url
        url_s = url[url.find("=")+1:url.rfind("&")]
        city = urllib.parse.unquote(url_s)
        tr_list = response.xpath("//div[@class='row']//tr")
        tr_list.pop(0)
        for tr in tr_list:
            item = AqiItem()
            item['city'] = city.decode('utf-8')
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

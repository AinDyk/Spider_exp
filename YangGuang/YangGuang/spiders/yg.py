# -*- coding: utf-8 -*-
import scrapy
from ..items import YangguangItem

class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ["http://wz.sun0769.com/index.php/question/questionType?type=4"]

    def parse(self, response):
        link_list = response.xpath("//div[@class='greyframe']/table[2]/tr/td/table/tr/td[2]/a[2]/@href").extract()
        for link in link_list:
            yield scrapy.Request(link,callback=self.parse_content)

        next_url = response.xpath("//a[text()='>']/@href").extract_first()
        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)

    def parse_content(self, response):
        item = YangguangItem()
        item['title'] = response.xpath('//title/text()').extract_first()[:-9]
        content = response.xpath("//div[@class='contentext']/text()").extract()
        item['num'] = response.xpath("//div[@class='cleft']/strong/text()").extract_first()[-6:]
        if len(content) == 0:
            content = response.xpath("//div[@class='c1 text14_2']/text()").extract()
            item['content'] = "".join(content).strip()
        else:
            item['content'] = "".join(content).strip()

        item['url'] = response.url
        yield item

# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import YangguangItem


class YgCSpider(CrawlSpider):
    name = 'yg_c'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=']

    rules = (
        Rule(LinkExtractor(allow=r'questionType\?type=4'), follow=True),
        Rule(LinkExtractor(allow=r'/html/question/\d+/\d+.shtml'), callback='parse_item'),

    )

    def parse_item(self, response):
        item = YangguangItem()
        item['title'] = response.xpath('//title/text()').extract_first()[:-9]
        content = response.xpath("//div[@class='contentext']/text()").extract()
        item['num'] = response.xpath("//div[@class='cleft']/strong/text()").extract_first().strip()[-6:]
        if len(content) == 0:
            content = response.xpath("//div[@class='c1 text14_2']/text()").extract()
            item['content'] = "".join(content).strip()
        else:
            item['content'] = "".join(content).strip()

        item['url'] = response.url
        yield item

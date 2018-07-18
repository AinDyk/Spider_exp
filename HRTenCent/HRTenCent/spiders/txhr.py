# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import HrtencentItem,DetailItem


class TxhrSpider(CrawlSpider):
    name = 'txhr'
    allowed_domains = ['hr.tencent.com']
    start_urls = ["http://hr.tencent.com/position.php?&start=0"]

    rules = (
        Rule(LinkExtractor(allow=r'start='), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/position_detail\.php\?id='), callback='parse_detail'),
    )

    def parse_item(self, response):
        tr_list = response.xpath(
            "//table[@class='tablelist']/tr[@class='even'] | //table[@class='tablelist']/tr[@class='odd']")
        for tr in tr_list:
            item = HrtencentItem()
            item['post_name'] = tr.xpath("./td[1]/a/text()").extract_first()
            item['post_link'] = "https://hr.tencent.com/" + tr.xpath("./td[1]/a/@href").extract_first()
            item['post_type'] = tr.xpath("./td[2]/text()").extract_first()
            item['peple_count'] = tr.xpath("./td[3]/text()").extract_first()
            item['post_local'] = tr.xpath("./td[4]/text()").extract_first()
            item['pub_times'] = tr.xpath("./td[5]/text()").extract_first()
            yield item

    def parse_detail(self,response):
        item = DetailItem()
        item['post_resp'] = response.xpath("//table[@class='tablelist textl']/tr[3]/td/ul//text()").extract()
        item['post_reqs'] = response.xpath("//table[@class='tablelist textl']/tr[4]/td/ul//text()").extract()
        yield item

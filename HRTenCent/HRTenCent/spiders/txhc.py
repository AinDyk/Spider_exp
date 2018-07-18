# -*- coding: utf-8 -*-
import scrapy
from ..items import HrtencentItem

class TxhcSpider(scrapy.Spider):
    name = 'txhc'
    allowed_domains = ['hr.tencent.com']
    # offset = 0
    # begin_url = "http://hr.tencent.com/position.php?&start="
    # start_urls = [base_url+str(offset)]
    # 通过start_urls处理高并发控制
    start_urls = ["http://hr.tencent.com/position.php?&start=" + str(num) for num in range(10,3761,10)]



    def parse(self, response):
        tr_list = response.xpath("//table[@class='tablelist']/tr[@class='even'] | //table[@class='tablelist']/tr[@class='odd']")
        for tr in tr_list:
            item = HrtencentItem()
            item['post_name'] = tr.xpath("./td[1]/a/text()").extract_first()
            item['post_link'] = "https://hr.tencent.com/" + tr.xpath("./td[1]/a/@href").extract_first()
            item['post_type'] = tr.xpath("./td[2]/text()").extract_first()
            item['peple_count'] = tr.xpath("./td[3]/text()").extract_first()
            item['post_local'] = tr.xpath("./td[4]/text()").extract_first()
            item['pub_times'] = tr.xpath("./td[5]/text()").extract_first()
            yield scrapy.Request(url=item['post_link'],callback=self.parse_detail,meta={"item":item})

        # 提取下一页url地址，并发送请求提取数据
        # if not response.xpath("//a[@id='next' and @class='noactive']/@href").extract_first():
        #     next_url = "https://hr.tencent.com/" + response.xpath("//a[@id='next']/@href").extract_first()
        #     yield scrapy.Request(next_url,callback=self.parse)
    #使用一个pipeline存储一个文件
    def parse_detail(self,response):
        item = response.meta['item']
        item['post_resp'] = response.xpath("//table[@class='tablelist textl']/tr[3]/td/ul//text()").extract()
        item['post_reqs'] = response.xpath("//table[@class='tablelist textl']/tr[4]/td/ul//text()").extract()
        yield item
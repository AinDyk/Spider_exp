# -*- coding: utf-8 -*-
import scrapy
import os
from ..items import SinaItem

class XlSpider(scrapy.Spider):
    name = 'xl'
    allowed_domains = ['sina.com.cn']
    start_urls = ["http://news.sina.com.cn/guide/"]

    def parse(self, response):
        items = []
        # 所有大类的url 和 标题
        parent_titles = response.xpath("//h3[@class='tit02']/a/text()").extract()
        parent_urls = response.xpath("//h3[@class='tit02']/a/@href").extract()

        # 所有小类的ur 和 标题
        sub_titles = response.xpath("//ul[@class='list01']/li/a/text()").extract()
        sub_urls = response.xpath("//ul[@class='list01']/li/a/@href").extract()

        # 爬取所有大类
        for i in range(0,len(parent_titles)):
            # 指定大类目录的路径和目录名
            parent_file_name = "./Data/" + parent_titles[i]
            # 如果目录不存在，则创建目录
            if not os.path.exists(parent_file_name):
                os.makedirs(parent_file_name)
            # 爬取所有小类
            for j in range(0,len(sub_titles)):
                item = SinaItem()
                item['parent_title'] = parent_titles[i]
                item['parent_url'] = parent_urls[i]

                # 检查小类的url是否以同类别大类url开头，如果是返回True (sports.sina.com.cn 和 sports.sina.com.cn/nba)
                isBelong = sub_urls[j].startswith(item['parent_url'])
                # 如果属于本大类，将存储目录放在本大类目录下
                if isBelong:
                    sub_file_name = parent_file_name + '/' + sub_titles[j]
                    # 如果目录不存在，则创建目录
                    if not os.path.exists(sub_file_name):
                        os.makedirs(sub_file_name)
                    # 存储 小类url、title和filename字段数据
                    item['sub_title'] = sub_titles[j]
                    item['sub_url'] = sub_urls[j]
                    item['sub_file_name'] = sub_file_name

                    items.append(item)
            # 发送每个小类url的Request请求，得到Response连同包含meta数据 一同交给回调函数 second_parse 方法处理
            for item in items:
                yield scrapy.Request(item['sub_url'],callback=self.second_parse,meta={'data_first':item})

    def second_parse(self,response):
        data_first = response.meta['data_first']

        # 取出小类里所有子链接
        link_list = response.xpath("//a/@href").extract()

        items = []
        for link in link_list:
            # 检查每个链接是否以大类url开头、以.shtml结尾，如果是返回True
            isBelong = link.startswith(data_first['parent_url']) and link.endswith('.shtml')
            # 如果属于本大类，获取字段值放在同一个item下便于传输
            if isBelong:
                item = SinaItem()
                item['parent_title'] = data_first['parent_title']
                item['parent_url'] = data_first['parent_url']
                item['sub_title'] = data_first['sub_title']
                item['sub_url'] = data_first['sub_url']
                item['sub_file_name'] = data_first['sub_file_name']
                item['son_url'] = link
                items.append(item)

        for item in items:
            yield scrapy.Request(item['son_url'],callback=self.third_parse,meta={'data_second':item})

    def third_parse(self,response):
        item = response.meta['data_second']
        # 数据解析方法，获取文章标题和内容
        head = response.xpath("//h1[@class='main-title']/text()").extract_first()
        content = response.xpath("//div[@class='article']/p/text()").extract()

        item['head'] = head
        item['content'] = "".join(content)

        yield item
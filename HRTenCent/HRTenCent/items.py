# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HrtencentItem(scrapy.Item):
    # define the fields for your item here like:
    # 岗位名称
    post_name = scrapy.Field()
    # 岗位的详情链接
    post_link = scrapy.Field()
    # 岗位类别
    post_type = scrapy.Field()
    # 岗位的招收人数
    peple_count = scrapy.Field()
    # 地点
    post_local = scrapy.Field()
    # 发布时间
    pub_times = scrapy.Field()
    # 数据源
    source = scrapy.Field()
    # 爬去时间
    spide_time = scrapy.Field()


class DetailItem(scrapy.Item):
    #岗位详情页中工作职责内容
    post_resp = scrapy.Field()
    #岗位详情页中工作要求
    post_reqs = scrapy.Field()
    # 数据源
    source = scrapy.Field()
    # 爬去时间
    spide_time = scrapy.Field()


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):
    # define the fields for your item here like:
    # 公司名
    name = scrapy.Field()
    # 公司类型
    type = scrapy.Field()
    # 公司主页
    home_page = scrapy.Field()
    # 标签
    tag = scrapy.Field()
    # 公司基本信息
    info = scrapy.Field()
    # 公司全名
    fullname = scrapy.Field()
    # 成立时间
    time = scrapy.Field()
    # 公司规模
    size = scrapy.Field()
    # 融资信息
    financing = scrapy.Field()
    # 团队信息
    team = scrapy.Field()


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AqiItem(scrapy.Item):
    # define the fields for your item here like:
    # 城市
    city = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # AQI
    aqi = scrapy.Field()
    # 质量等级
    level = scrapy.Field()
    # PM2.5
    pm2_5 = scrapy.Field()
    # PM10
    pm10 = scrapy.Field()
    # SO2
    so2 = scrapy.Field()
    # CO
    co = scrapy.Field()
    # NO2
    no2 = scrapy.Field()
    # O3_8h
    o3 = scrapy.Field()

    # 抓取时间
    crawl_time = scrapy.Field()
    # 数据源
    source = scrapy.Field()

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    # 大类的标题 和 url
    parent_title = scrapy.Field()
    parent_url = scrapy.Field()

    # 小类的标题 和 子url
    sub_title = scrapy.Field()
    sub_url = scrapy.Field()

    # 小类目录存储路径
    sub_file_name = scrapy.Field()

    # 小类下的子链接
    son_url = scrapy.Field()

    # 文章标题和内容
    head = scrapy.Field()
    content = scrapy.Field()



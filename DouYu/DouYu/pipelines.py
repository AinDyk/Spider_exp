# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from .settings import IMAGES_STORE
from datetime import datetime
import scrapy
import logging
import pymongo
import os

class DouYuImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_src'])

    def item_completed(self, results, item, info):
        old_image_path = [x['path'] for ok,x in results if ok][0]
        new_name = IMAGES_STORE + item['nick_name'] +'.jpg'
        item['image_path'] = new_name
        try:
            os.rename(IMAGES_STORE + old_image_path, item['image_path'])
        except:
            logging.error("图片已被修改....")

        return item


class DouYuMongoPipeline(object):
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host='localhost',port=27017)
        self.db = self.client['Douyu']
        self.collection = self.db['item']

    def process_item(self,item,spider):
        item['crawl_time'] = str(datetime.now())
        item['source'] = spider.name
        self.collection.insert(dict(item))
        return item
#
# class DouyuPipeline(object):
#     def process_item(self, item, spider):
#         return item

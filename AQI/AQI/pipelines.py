# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from scrapy.exporters import CsvItemExporter
import json
import pymongo

class AqiPipeline(object):
    def process_item(self, item, spider):
        item['crawl_time'] = str(datetime.utcnow())
        item['source'] = spider.name
        return item

class CsvPipeline(object):
    def open_spider(self,spider):
        self.file = open('aqi_csv.csv','wb')
        self.csv = CsvItemExporter(self.file)
        self.csv.start_exporting()

    def process_item(self,item,spider):
        self.csv.export_item(item)
        return item

    def close_item(self,spider):
        self.csv.finish_exporting()
        self.file.close()

class JsonPipeline(object):
    def open_spider(self,spider):
        self.file = open('aqi_item.json','w')

    def process_item(self,item,spider):
        self.file.write(json.dumps(dict(item)) + ',\n')
        return item

    def close_spider(self,spider):
        self.file.close()

class MongoPipeline(object):
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host='localhost',port=27017)
        self.db = self.client['AQI']
        self.connection = self.db['item']

    def process_item(self,item,spider):
        self.connection.insert(dict(item))
        return item


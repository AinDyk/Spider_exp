# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from .items import HrtencentItem,DetailItem
from datetime import datetime


class HrtencentPipeline(object):
    def open_spider(self,spider):
        self.save_file = open("tencent_hr.json","w")
    def process_item(self, item, spider):
        if isinstance(item,HrtencentItem):
            item['source'] = spider.name
            item['spide_time'] = str(datetime.now())
            content = json.dumps(dict(item)) + "\n"
            self.save_file.write(content)
        return item

    def close_spider(self,spider):
        self.save_file.close()


class DetailPipeline(object):
    def open_spider(self,spider):
        self.save_file = open("tencent_hr_detail.json","w")
    def process_item(self, item, spider):
        if isinstance(item,DetailItem):
            item['source'] = spider.name
            item['spide_time'] = str(datetime.now())
            content = json.dumps(dict(item)) + "\n"
            self.save_file.write(content)
        return item

    def close_spider(self,spider):
        self.save_file.close()

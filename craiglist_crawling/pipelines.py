# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#https://realpython.com/blog/python/web-scraping-with-scrapy-and-mongodb/

class CraiglistPipeline(object):
    def process_item(self, item, spider):
        return item

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json

class ToiCrawlerPipeline(object):

    def __init__(self):
        self.j = 0
    
    def process_item(self, item, spider):
        self.j=self.j+1
        self.file = open('toi_sports_cricket_%s.jl'%self.j, 'wb')
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

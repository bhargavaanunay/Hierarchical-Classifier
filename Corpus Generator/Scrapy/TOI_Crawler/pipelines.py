# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import os
import json
from TOI_Crawler.path_fixer import fix_path

class ToiCrawlerPipeline(object):

    def __init__(self):
        self.j = 0
        print "\nEnter ABSOLUTE path of top directory of Corpus:",
        self.path = raw_input()
        if self.path[-1] == '/':
            self.path = self.path[:-1]
        print "\nEnter specific category:",
        self.category = raw_input()
        print
        complete_path = self.path + '/' + self.category
        path_broad = complete_path[:complete_path.rfind('/')]
        fix_path(path_broad)
        fix_path(complete_path)
    
    def process_item(self, item, spider):
        self.j=self.j+1
        self.file = open('%s/%s/%s.jl'%(self.path,self.category,self.j), 'wb')
        item_dict = dict(item)
        line = json.dumps(item_dict) + "\n"
        if self.j == 1:
            print "\n\nSaved data:\n"
        print str(self.j) + '\t' + item_dict['title'][0]
        self.file.write(line)
        return item

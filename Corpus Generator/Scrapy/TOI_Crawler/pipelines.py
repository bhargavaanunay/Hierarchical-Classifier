# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from TOI_Crawler.path_fixer import fix_path
import json

class ToiCrawlerPipeline(object):

    def __init__(self):
        self.j = 0
        print "\nEnter ABSOLUTE path of top directory of Corpus:",
        self.path = raw_input()
        if self.path[-1] == '/':
            self.path = self.path[:-1]
        print "\nEnter broad category:",
        broad = raw_input()
        print "\nEnter specific category:",
        specific = raw_input()
        self.category = broad + '/' + specific
        complete_path = self.path + '/' + broad + '/' + specific
        fix_path(complete_path)
        print "\nEnter limit on number of articles to be saved:",
        self.limit = int(raw_input())
        print        
    
    def process_item(self, item, spider):
        if self.j == self.limit and not spider.close_down:
            print "\n\nTask Successfully completed!\n"
            spider.close_down = True
        else:
            self.j = self.j + 1
            file = open('%s/%s/%s.jl' % (self.path, self.category, self.j), 'wb')
            item_dict = dict(item)
            line = json.dumps(item_dict) + "\n"
            if self.j == 1:
                print "\n\nSaved data:\n"
            print str(self.j) + '\t' + item_dict['title'][0]
            file.write(line)
        return item
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from TOI_Crawler.items import ToiCrawlerItem
from TOI_Crawler.path_fixer import fix_path
import os

class ToiCrawlerSpider(BaseSpider):

    name = "Toi"
    allowed_domains = ["timesofindia.indiatimes.com"]
    os.system('clear')
    print "Enter URL of a seed page (page of an article, not a topic):",
    seed = raw_input()
    start_urls = [seed]
    idx1 = seed.find('.com/') + 5
    idx2 = seed.find('/', idx1 + 1)
    idx2 = seed.find('/', idx2 + 1)
    sp_category = seed[idx1:idx2]
    links_with_error = []
    print "\nEnter ABSOLUTE path of the directory where you want the error file to be saved:",
    err_links_file_loc = raw_input()
    err_count = 0
    fix_path(err_links_file_loc)
    if err_links_file_loc[-1] == '/':
        err_links_file_loc = err_links_file_loc[:-1]

    def parse(self, response):
        w = ToiCrawlerItem()
        currentURL = response.url
        if currentURL.find('/articleshow/') != -1:
            hxs = HtmlXPathSelector(response)
            title = hxs.select('//title/text()').extract()
            w['title']= title
            content = hxs.select('//tmp/text()').extract()
            content1 = str(content)
            if content1.find('a') == -1:
                 con = hxs.select('//div[contains(@class,"Normal")]')
                 if len(con) > 1:
                     self.links_with_error.append(currentURL)
                 else:
                     content = con.select('text()').extract()
                     w['content'] = content
                     w['url'] = currentURL
                     yield w
            else:
                 w['content'] = content
                 w['url'] = currentURL
                 yield w
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//a[contains(@href,"/%s")]/@href' % self.sp_category).extract()
        for site in sites:
            site = str(site)
            idx = site.rfind('?')
            if idx != -1:
                site = site[:idx]
            if site.find('/videos/') == -1:
                 if site.find('http://')==-1:
                    site = "http://timesofindia.indiatimes.com" + site
                    # May help to debug: print site
                    yield Request(site, callback=self.parse)
                 else:
                    yield Request(site, callback=self.parse)
        if self.err_count == 0:
            error_file = open('%s/0_error_pages.txt' % self.err_links_file_loc, 'w')
            error_file.close()
        error_file = open('%s/0_error_pages.txt' % self.err_links_file_loc, 'a')
        with error_file:
            for link in self.links_with_error:
                error_file.write(link + '\n')
                self.err_count = self.err_count + 1
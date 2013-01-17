from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from TOI_Crawler.items import ToiCrawlerItem

class ToiCrawlerSpider(BaseSpider):

    name = "Toi"
    allowed_domains = ["timesofindia.indiatimes.com"]
    print "\nEnter URL of a seed page (page of an article, not a topic):"
    seed = raw_input()
    start_urls = [seed]
    idx1 = seed.find('.com/') + 5
    idx2 = seed.find('/', idx1 + 1)
    idx2 = seed.find('/', idx2 + 1)
    sp_category = seed[idx1:idx2]

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
                     print "\n\n\nHELLO HELLO HELLO\n\n\n"
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
            if site.find('video/%s' % self.sp_category) == -1:
                 if site.find('http://')==-1:
                    site = "http://timesofindia.indiatimes.com" + site
                    print "\n\n\n", site, "\n\n\n"
                    yield Request(site, callback=self.parse)
                 else:
                    yield Request(site, callback=self.parse)             
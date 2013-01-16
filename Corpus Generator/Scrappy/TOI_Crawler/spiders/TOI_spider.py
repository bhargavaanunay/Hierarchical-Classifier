from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from TOI_Crawler.items import ToiCrawlerItem
    

class ToiCrawlerSpider(BaseSpider):

    name = "Toi"
    allowed_domains = ["timesofindia.indiatimes.com"]
    start_urls = [
        "http://timesofindia.indiatimes.com/sports/cricket/sphome/4719161.cms",]

    def parse(self, response):
        #print "\n\n\n\n\nRESPONSE ",response.url,"\n\n\n\n\n"
        w=ToiCrawlerItem()
        currentURL = response.url
        #print "\n\n\n",currentURL,"\n\n\n"
        if  currentURL.find('/articleshow/')!=-1:
            hxs = HtmlXPathSelector(response)
            title = hxs.select('//title/text()').extract()
            #print "\n\n\n",title,"\n\n\n"
            w['title']= title
            content = hxs.select('//tmp/text()').extract()
            #print "\n\n\n",content, "\n\n\n"
            content1=str(content)
            if content1.find('a')==-1:
                 con = hxs.select('//div[contains(@class,"Normal")]')
                 if len(con)>1:
                     print "\n\n\nHELLO HELLO HELLO\n\n\n"
                 else:
                     content=con.select('text()').extract()
                     w['content'] = content
                     w['url']=currentURL
                     yield  w
            else:
                 w['content']=content
                 w['url']=currentURL
                 yield w
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//a[contains(@href,"/sports/cricket")]/@href').extract()
        
        for site in sites:
            #print "\n\n\n",site,"\n\n\n"
            #u=site.select('@href').extract()
            #print "\n\n\n",u[0],"\n\n\n"
            site=str(site)
            #print "\n\n\n",site,"\n\n\n"
            if site.find('video/sports/cricket')== -1:
                 if site.find('http://')==-1:
                    site= "http://timesofindia.indiatimes.com"+ site
                    print "\n\n\n", site, "\n\n\n"
                    yield Request(site, callback=self.parse)
                 else:
                    yield Request(site,callback=self.parse) 
            
           
            #s="http://timesofindia.indiatimes.com/sports/cricket/top-stories/2nd-Test-South-Africa-complete-innings-win-over-New-Zealand/articleshow/18019385.cms"
                   
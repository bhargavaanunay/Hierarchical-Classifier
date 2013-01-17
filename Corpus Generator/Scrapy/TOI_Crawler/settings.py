# Scrapy settings for TOI_Crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'TOI_Crawler'

SPIDER_MODULES = ['TOI_Crawler.spiders']
NEWSPIDER_MODULE = 'TOI_Crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'TOI_Crawler (+http://www.yourdomain.com)'

DEFAULT_ITEM_CLASS = 'TOI_Crawler.items.ToiCrawlerItem'

ITEM_PIPELINES = ['TOI_Crawler.pipelines.ToiCrawlerPipeline']
DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter'

LOG_LEVEL = 'INFO'


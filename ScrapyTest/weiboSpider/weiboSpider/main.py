from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from weiboSpider.spiders.weibo_com import WeiboComSpider

if __name__=='__main__':
    process = CrawlerProcess(get_project_settings())
    # process.crawl('cnblogs_itemloader')
    process.crawl('weibo.com')
    process.start()

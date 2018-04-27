from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__=='__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('weibo.com_PhantomJS')
    # process.crawl('weibo.com')
    process.start()

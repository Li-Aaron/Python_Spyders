# -*- coding: utf-8 -*-

# Scrapy settings for vkSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import ConfigParser

BOT_NAME = 'vkSpider'

SPIDER_MODULES = ['vkSpider.spiders']
NEWSPIDER_MODULE = 'vkSpider.spiders'

# for vk login and start urls
def album_parse(album_urls):
    album_urls = album_urls.strip('[').strip(']').split(',')
    fun = lambda x:x.strip('\n').strip('\'').strip('\"')
    return [fun(x) for x in album_urls if fun(x)]

conf = ConfigParser.ConfigParser()
conf.read('settings.cfg')

USERNAME = conf.get('user','username')
PASSWORD = conf.get('user','password')

ALBUM_URLS = album_parse(conf.get('urls','album'))


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'vkSpider (+http://www.yourdomain.com)'
USER_AGENTS = [
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.0', # Firefox Windows
    # 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0', # Firefox Windows
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36', # Chrome Windows
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240' # Edge Windows
    # 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1' # Safari Iphone
]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
# COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'vkSpider.middlewares.VkspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'vkSpider.middlewares.RandomUserAgent': 450,
    # 'vkSpider.middlewares.RandomProxy': 460,
    'vkSpider.middlewares.FixedProxy': 460,
    'vkSpider.middlewares.ChromeMiddleware': 470,
}
PROXY = 'http://127.0.0.1:3213'

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    # 'scrapy.extensions.telnet.TelnetConsole': None,
    'vkSpider.extensions.SpiderStatus': 0,
}
MYEXT_ENABLED = True
MYEXT_ITEMCOUNT = 100


# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'vkSpider.pipelines.VkSpiderPipeline': 300,
    'vkSpider.pipelines.VkImagesPipeline': 200,
}
# MongoItemPipeline Settings
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'vk'
# ImagesPipeline Settings
IMAGES_STORE = '.\\Images'
IMAGES_URLS_FIELD = 'image_url'
IMAGES_RESULT_FIELD = 'images'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# LOG setting
LOG_FILE = 'vk.log'
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_LEVEL = 'INFO'
# LOG_FORMAT = '[%(asctime)s][%(name)s: %(processName)s(%(process)s): %(threadName)s: %(funcName)s] %(levelname)s : %(message)s'
LOG_FORMAT = '[%(asctime)s][%(name)s: %(funcName)s] %(levelname)s : %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
# LOG_STDOUT = True
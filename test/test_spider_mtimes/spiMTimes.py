# -*- coding: utf-8 -*-
'''
程序名称 spyMTimes
@Author: AC
2018-3-12
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
from WebSpiCommon import HtmlDownloader
from HtmlParser import HtmlParser
from DataOutput import DataOutput
import time
import traceback
from WebSpiCommon import logger, Schedule

##############################################
#------------------常量定义------------------#
##############################################
URL = 'http://theater.mtime.com/China_Shanghai/'


##############################################
#------------------函数定义------------------#
##############################################

##############################################
#------------------类定义--------------------#
##############################################
class spiMTimes(object):
    def __init__(self):
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def Crawl(self, root_url):
        '''
        Start Crawling from first url
        :param root_url: the first url
        :param max_size: max crawling url num
        :return:
        '''
        content = self.downloader.OpenWebPage(root_url)
        logger.debug('root url: %s' % (root_url,))
        urls = self.parser.parser_urls(content)
        # 构造获取票房链接
        idx = 1
        for url in urls:
            try:
                t = time.strftime("%Y%m%d%H%M%S1357", time.localtime())
                rank_url = 'http://service.library.mtime.com/Movie.api'\
                           '?Ajax_CallBack=true'\
                           '&Ajax_CallBackType=Mtime.Library.Services'\
                           '&Ajax_CallBackMethod=GetMovieOverviewRating'\
                           '&Ajax_CrossDomain=1'\
                           '&Ajax_RequestUrl=%s'\
                           '&t=%s'\
                           '&Ajax_CallBackArgument0=%s'\
                           %(url[0],t,url[1])
                logger.debug('rank url: %s' % (rank_url,))
                rank_content = self.downloader.OpenWebPage(rank_url)
                logger.debug('rank content: %s' % (rank_content,))
                data = self.parser.parser_json(rank_url, rank_content)
                self.output.StoreData(data)
                Schedule(idx, len(urls))
                idx += 1
            except Exception,e:
                print "Crawl failed"
                logger.error(repr(e))
                logger.error(traceback.format_exc())
        del self.output
        print "Crawl finish"



##############################################
#------------------脚本开始------------------#

##############################################
if __name__ == '__main__':
    # argv check
    spi = spiMTimes()
    spi.Crawl(URL)


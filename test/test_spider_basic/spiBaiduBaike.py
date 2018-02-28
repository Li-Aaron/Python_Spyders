# -*- coding: utf-8 -*-
'''
程序名称 spyBaiduBaike
@Author: AC
2018-2-26
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
from WebSpiCommon import HtmlDownloader
from WebSpiCommon import HtmlParser
from WebSpiCommon import DataOutput
from WebSpiCommon import UrlManager

##############################################
#------------------常量定义------------------#
##############################################
URL = 'https://baike.baidu.com/item/网络爬虫/5162711'


##############################################
#------------------函数定义------------------#
##############################################
def Schedule(num, totalNum, printFlg = True, note = ''):
    process = 100.0 * num / totalNum
    note = '(%s)'% note if note else ''
    if printFlg:
        print "[%4.3f%%] %5d of %5d is done %s..." % (process, num, totalNum, note)
    return process

##############################################
#------------------类定义--------------------#
##############################################
class spiBaiduBaike(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def Crawl(self, root_url, max_size = 100):
        '''
        Start Crawling from first url
        :param root_url: the first url
        :param max_size: max crawling url num
        :return:
        '''
        self.manager.AddNewUrl(root_url)
        while(self.manager.HasNewUrl() and self.manager.OldUrlSize() < max_size):
            try:
                # 获取新URL
                new_url = self.manager.GetNewUrl()
                # 打开网页 获取html
                html = self.downloader.OpenWebPage(new_url)
                # 解析html 获取新URL和数据
                new_urls, data = self.parser.Parser(new_url, html)
                # 将抽取的URL 添加到URL管理器中
                self.manager.AddNewUrls(new_urls)
                # 存储数据
                self.output.StoreData(data)
                # 打印进度信息
                Schedule(self.manager.OldUrlSize(), max_size, note=data['title'])
            except Exception as e:
                print e
                print "crawl failed"
        self.output.SaveHtml("BaikeCrawled.html",title="Baike Crawled")
        self.output.SaveCsv("BaikeCrawled.csv")


##############################################
#------------------脚本开始------------------#

##############################################
if __name__ == '__main__':
    # argv check
    spi = spiBaiduBaike()
    spi.Crawl(URL,max_size = 500)


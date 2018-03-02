# -*- coding: utf-8 -*-
'''
程序名称 spiBaiduBaikeNode

UrlManagerProc    --(url)--->   Node(Slave)
      ↑
    (url)
      |
ResultSolveProc  <--(data)--    Node(Slave)
      |
    (data)
      ↓
DataOutputProc    --(data)-->   HtmlFile

@Author: AC
2018-3-1
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
from multiprocessing import Queue,Process
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support

from WebSpiCommon import HtmlDownloader
from WebSpiCommon import HtmlParser
import chardet
import time

# log 日志记录
import logging
import logging.config
import yaml

log_conf = './logger.yml'
with open(log_conf, 'rt') as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)
logger = logging.getLogger('node')

##############################################
#------------------常量定义------------------#
##############################################
MANAGER_IP = '127.0.0.1'
MANAGER_PORT = 8001


##############################################
#------------------函数定义------------------#
##############################################
def ToUTF8(content):
    if isinstance(content, unicode):
        return content.encode('utf-8')
    else:
        return content.decode(chardet.detect(content)['encoding']).encode('utf-8')

##############################################
#------------------类定义--------------------#
##############################################
class SpiNode(object):

    def __init__(self):
        # initialize node connection
        # register方法将队列获取注册名
        BaseManager.register('get_url_queue')
        BaseManager.register('get_result_queue')

        # connect to manager
        logger.info('Connect to server %s' %(MANAGER_IP,))
        self.manager = BaseManager(address=(MANAGER_IP,MANAGER_PORT), authkey='spiBaiduBaike')
        self.manager.connect()

        # 通过管理实例的方法获得通过网络访问的Queue对象
        self.q_url = self.manager.get_url_queue()
        self.q_result = self.manager.get_result_queue()

        # init downloader and parser
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        logger.info('Node Start Finish')

    def Crawl(self):
        while True:
            try:
                # url <-- Manager(UrlManagerProc)
                if self.q_url.empty():
                    logger.warn('No url in Queue')
                elif self.q_result.full():
                    logger.warn('Result Queue Full')
                else:
                    url = self.q_url.get()
                    # end --> Manager(ResultSolveProc)
                    if url == 'end':
                        self.q_url.put('end', timeout=1)  # notify other nodes
                        time.sleep(3) # 保证每个节点都下载完了(应该有更好的方法)
                        logger.info('Put ending to Manager')
                        content = {'new_urls':'end','data':'end'}
                        self.q_result.put(content, timeout = 1)
                        return
                    # content --> Manager(ResultSolveProc)
                    logger.info('Node Crawling %s'%(ToUTF8(url),))
                    html_content = self.downloader.OpenWebPage(url)
                    new_urls, data = self.parser.Parser(url, html_content)
                    logger.info('Node Crawled %s' % (ToUTF8(data['title']),))
                    content = {"new_urls":new_urls,"data":data}
                    self.q_result.put(content, timeout = 1)
                time.sleep(0.1)
            except EOFError, e:
                logger.error('Connection Error')
                return
            except Exception, e:
                logger.error('Crawling Failed')
                logger.error(e)
                time.sleep(0.5)

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    spider = SpiNode()
    spider.Crawl()


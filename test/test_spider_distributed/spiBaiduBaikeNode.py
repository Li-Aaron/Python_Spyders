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
import LogPrint

import time
##############################################
#------------------常量定义------------------#
##############################################
MANAGER_IP = '127.0.0.1'
MANAGER_PORT = 8001
LOG_CONTROL = LogPrint.INFO|LogPrint.ERROR|LogPrint.DEBUG|LogPrint.DISP|LogPrint.FILE
LOG_FILENAME = 'node_log_%s.txt' % (time.strftime("%Y%m%d_%H%M%S",time.localtime()),)

##############################################
#------------------函数定义------------------#
##############################################
def Schedule(num, totalNum, printFlg = True, note = ''):
    process = 100.0 * num / totalNum
    note = '(%s)'% note if note else ''
    if printFlg:
        print "[%4.3f%%] %5d of %5d is done %s..." % (process, num, totalNum, note)
    return process

def Log(content, log_type):
    LogPrint.LogPrint(content, log_type=log_type, log_control=LOG_CONTROL, filename=LOG_FILENAME)


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
        Log('Connect to server %s' %(MANAGER_IP,), log_type=LogPrint.INFO)
        self.manager = BaseManager(address=(MANAGER_IP,MANAGER_PORT), authkey='spiBaiduBaike')
        self.manager.connect()

        # 通过管理实例的方法获得通过网络访问的Queue对象
        self.q_url = self.manager.get_url_queue()
        self.q_result = self.manager.get_result_queue()

        # init downloader and parser
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        Log('Node Start Finish', log_type=LogPrint.INFO)

    def Crawl(self):
        while True:
            try:
                # url <-- Manager(UrlManagerProc)
                if self.q_url.empty():
                    Log('No url in Queue', log_type=LogPrint.DEBUG)
                elif self.q_result.full():
                    Log('Result Queue Full', log_type=LogPrint.DEBUG)
                else:
                    url = self.q_url.get()
                    # end --> Manager(ResultSolveProc)
                    if url == 'end':
                        Log('Put ending to Manager', log_type=LogPrint.INFO)
                        content = {'new_urls':'end','data':'end'}
                        self.q_result.put(content, timeout = 1)
                        return
                    # content --> Manager(ResultSolveProc)
                    Log('Node Crawling %s'%(LogPrint.ToUTF8(url),), log_type=LogPrint.INFO)
                    html_content = self.downloader.OpenWebPage(url)
                    new_urls, data = self.parser.Parser(url, html_content)
                    Log('Node Crawled %s' % (LogPrint.ToUTF8(data['title']),), log_type=LogPrint.INFO)
                    content = {"new_urls":new_urls,"data":data}
                    self.q_result.put(content, timeout = 1)
                time.sleep(0.1)
            except EOFError, e:
                Log('Connection Error', log_type=LogPrint.ERROR)
                return
            except Exception, e:
                Log('Crawling Failed', log_type=LogPrint.ERROR)
                time.sleep(0.5)

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    spider = SpiNode()
    spider.Crawl()


# -*- coding: utf-8 -*-
'''
程序名称 spiBaiduBaikeManager

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

from WebSpiCommon import DataOutput
from WebSpiCommon import UrlManager

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
logger = logging.getLogger('manager')
##############################################
#------------------常量定义------------------#
##############################################
URL = 'https://baike.baidu.com/item/网络爬虫/5162711'
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
class SpiManager(object):

    def __init__(self, root_url, max_crawl_size = 100):
        self.root_url = root_url
        self.max_crawl_size = max_crawl_size

    def StartManager(self, queue_url, queue_result):
        '''
        distributed manager (main process)
        :param queue_url: url 队列（外部）
        :param queue_result: 结果队列（外部）
        :return: manager object
        '''
        # windows下多进程可能会有问题，添加这句可以缓解
        freeze_support()

        # register方法将队列获取注册名
        BaseManager.register('get_url_queue', callable=lambda:queue_url)
        BaseManager.register('get_result_queue', callable=lambda:queue_result)

        # 绑定端口8001，注册密码
        manager = BaseManager(address=(MANAGER_IP, MANAGER_PORT), authkey='spiBaiduBaike')

        return manager

    def UrlManagerProc(self, queue_url, queue_conn):
        '''
        url manager process
        :param queue_url: url 队列（外部）
        :param queue_conn: 获取队列（内部）
        :param root_url: 初始地址
        :return:
        '''
        url_manager = UrlManager()
        url_manager.AddNewUrl(self.root_url)
        idx = 1
        # FOREVER
        while True:
            # put all new_urls --> node
            while(url_manager.HasNewUrl()):
                if not queue_url.full():
                    # get a new url from url manager
                    new_url = url_manager.GetNewUrl()
                    # url --> node
                    queue_url.put(new_url, timeout = 1)
                    logger.debug('[%04d]Put Url: %s' % (idx,ToUTF8(new_url),))
                    idx += 1
                    # Log('[UrlManagerProc]Old Url Size: %s' % (url_manager.OldUrlSize(),), log_type=LogPrint.DEBUG)
                    if(url_manager.OldUrlSize() >= self.max_crawl_size):
                        # end --> node
                        queue_url.put('end', timeout = 1)
                        logger.info('Put ending to Node')
                        # save progress
                        url_manager.SaveProgress(url_manager.new_urls,filename='new_urls.txt')
                        url_manager.SaveProgress(url_manager.old_urls,filename='old_urls.txt')
                        return
                else:
                    logger.warn('Url Queue Full')
                    break # 这里要退出while 不然会导致Connection Queue满掉
            # get new_urls <-- ResultSolveProc
            try:
                if not queue_conn.empty():
                    urls = queue_conn.get(True, timeout = 1)
                    logger.debug('Get %s Urls from ResultSolveProc'%(len(urls),))
                    url_manager.AddNewUrls(urls)
                else:
                    logger.info('Connection Queue Empty (No url get from ResultSolveProc)')
                    time.sleep(0.5)
            except BaseException,e:
                logger.error(e)
                time.sleep(0.5)

    def ResultSolveProc(self, queue_conn, queue_result, queue_store):
        '''
        result solve, result --> output proc, new_url --> url manager
        :param queue_conn: 获取队列（内部）
        :param queue_result: 结果队列（外部）
        :param queue_store: 存储队列（内部）
        :return:
        '''
        crawled_url = 0
        while True:
            try:
                if queue_result.empty():
                    logger.info('Result Queue Empty (No content get from Node)')
                    time.sleep(0.5)
                elif queue_store.full():
                    logger.warn('Storage Queue Full')
                    time.sleep(0.5)
                elif queue_conn.full() and crawled_url < self.max_crawl_size:
                    # 在没有爬完的情况下队列满了
                    logger.info('Connection Queue Full / not finish')
                    time.sleep(0.5)
                else:
                    content = queue_result.get(True, timeout=1)
                    # end <-- node
                    if content['new_urls'] == 'end':
                        logger.info('Ending from Node')
                        # end --> store
                        queue_store.put('end', timeout=1)
                        return
                    crawled_url += len(content['new_urls'])
                    logger.debug('Solve %s urls, %s' %(crawled_url,ToUTF8(content['data']['title'])))
                    if not queue_conn.full():
                        queue_conn.put(content['new_urls'], timeout=1)
                    else:
                        # 在已经爬完的情况下队列满了
                        logger.info('Connection Queue Full / finished')
                    queue_store.put(content['data'], timeout=1)
            except BaseException, e:
                logger.error(e)
                time.sleep(0.5)

    def DataOutputProc(self, queue_store):
        '''
        save data to html file
        :param queue_store: 存储队列（内部）
        :return:
        '''
        idx = 1
        output = DataOutput(filename='BaikeCrawled.html', title='BaikeCrawled')
        while True:
            if not queue_store.empty():
                data = queue_store.get(True, timeout = 1)
                if data == 'end':
                    logger.info('Ending from ResultSolveProc')
                    del output
                    return
                output.StoreData(data)
                logger.info('[%04d]store %s' % (idx,ToUTF8(data['title'])))
                idx += 1
            else:
                logger.info('Store Queue Empty(No data get from ResultSolveProc)')
                time.sleep(0.5)

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # init queue
    max_queue_size = 200
    max_crawl_size = 2000
    queue_url = Queue(max_queue_size)
    queue_result = Queue(max_queue_size)
    queue_conn = Queue(max_queue_size)
    queue_store = Queue(max_queue_size)

    # create distributed manager
    sm = SpiManager(URL, max_crawl_size)
    manager = sm.StartManager(queue_url=queue_url, queue_result=queue_result)

    # create processes
    url_manager_proc = Process(target=sm.UrlManagerProc, args=(queue_url, queue_conn),name='UrlManagerProc')
    result_solve_proc = Process(target=sm.ResultSolveProc, args=(queue_conn, queue_result, queue_store),name='ResultSolveProc')
    data_output_proc = Process(target=sm.DataOutputProc, args=(queue_store,),name='DataOutputProc')

    # start processes and manager
    url_manager_proc.start()
    result_solve_proc.start()
    data_output_proc.start()
    manager.get_server().serve_forever()

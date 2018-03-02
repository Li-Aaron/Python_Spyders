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
import LogPrint

import time
##############################################
#------------------常量定义------------------#
##############################################
URL = 'https://baike.baidu.com/item/网络爬虫/5162711'
MANAGER_IP = '127.0.0.1'
MANAGER_PORT = 8001
LOG_CONTROL = LogPrint.INFO|LogPrint.ERROR|LogPrint.DEBUG|LogPrint.DISP
LOG_FILENAME = 'manager_log_%s.txt' % (time.strftime("%Y%m%d_%H%M%S",time.localtime()),)

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
class SpiManager(object):

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

    def UrlManagerProc(self, queue_url, queue_conn, root_url = URL, max_crawl_size = 2000):
        '''
        url manager process
        :param queue_url: url 队列（外部）
        :param queue_conn: 获取队列（内部）
        :param root_url: 初始地址
        :return:
        '''
        url_manager = UrlManager()
        url_manager.AddNewUrl(root_url)
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
                    Log('[UrlManagerProc][%04d]Put Url: %s' % (idx,LogPrint.ToUTF8(new_url),), log_type=LogPrint.DEBUG)
                    idx += 1
                    # Log('[UrlManagerProc]Old Url Size: %s' % (url_manager.OldUrlSize(),), log_type=LogPrint.DEBUG)
                    if(url_manager.OldUrlSize() > max_crawl_size):
                        # end --> node
                        queue_url.put('end', timeout = 1)
                        Log('Put ending to Node', log_type=LogPrint.INFO)
                        # save progress
                        url_manager.SaveProgress('new_urls.txt',url_manager.new_urls)
                        url_manager.SaveProgress('old_urls.txt',url_manager.old_urls)
                        return
                else:
                    Log('[UrlManagerProc]Url Queue Full', log_type=LogPrint.DEBUG)
                    break # 这里要退出while 不然会导致Connection Queue满掉
            # get new_urls <-- ResultSolveProc
            try:
                if not queue_conn.empty():
                    urls = queue_conn.get(True, timeout = 1)
                    Log('[UrlManagerProc]Get %s Urls from ResultSolveProc'%(len(urls),), log_type=LogPrint.DEBUG)
                    url_manager.AddNewUrls(urls)
                else:
                    Log('[UrlManagerProc]Connection Queue Empty (No url get from ResultSolveProc)', log_type=LogPrint.DEBUG)
                    time.sleep(0.5)
            except BaseException,e:
                Log('[UrlManagerProc]', log_type=LogPrint.ERROR)
                time.sleep(0.5)

    def ResultSolveProc(self, queue_conn, queue_result, queue_store):
        '''
        result solve, result --> output proc, new_url --> url manager
        :param queue_conn: 获取队列（内部）
        :param queue_result: 结果队列（外部）
        :param queue_store: 存储队列（内部）
        :return:
        '''
        while True:
            try:
                if queue_result.empty():
                    Log('[ResultSolveProc]Result Queue Empty (No content get from Node)', log_type=LogPrint.DEBUG)
                    time.sleep(0.5)
                elif queue_store.full():
                    Log('[ResultSolveProc]Storage Queue Full', log_type=LogPrint.DEBUG)
                    time.sleep(0.5)
                elif queue_conn.full():
                    Log('[ResultSolveProc]Connection Queue Full', log_type=LogPrint.DEBUG)
                    time.sleep(0.5)
                else:
                    content = queue_result.get(True, timeout=1)
                    # end <-- node
                    if content['new_urls'] == 'end':
                        Log('ResultSolveProc ending from Node', log_type=LogPrint.INFO)
                        # end --> store
                        queue_store.put('end', timeout=1)
                        return
                    Log('[ResultSolveProc]Solve %s urls, %s' %(len(content['new_urls']),LogPrint.ToUTF8(content['data']['title'])), log_type=LogPrint.DEBUG)
                    queue_conn.put(content['new_urls'], timeout=1)
                    queue_store.put(content['data'], timeout=1)
            except BaseException, e:
                Log('[ResultSolveProc]', log_type=LogPrint.ERROR)
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
                    Log('DataOutputProc ending from ResultSolveProc', log_type=LogPrint.INFO)
                    del output
                    return
                output.StoreData(data)
                Log('[DataOutputProc][%04d]store %s' % (idx,LogPrint.ToUTF8(data['title'])), log_type=LogPrint.INFO)
                idx += 1
            else:
                Log('[DataOutputProc]Store Queue Empty(No data get from ResultSolveProc)', log_type=LogPrint.DEBUG)
                time.sleep(0.5)

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # init queue
    max_size = 200
    queue_url = Queue(max_size)
    queue_result = Queue(max_size)
    queue_conn = Queue(max_size)
    queue_store = Queue(max_size)

    # create distributed manager
    sm = SpiManager()
    manager = sm.StartManager(queue_url=queue_url, queue_result=queue_result)

    # create processes
    url_manager_proc = Process(target=sm.UrlManagerProc, args=(queue_url, queue_conn, URL))
    result_solve_proc = Process(target=sm.ResultSolveProc, args=(queue_conn, queue_result, queue_store))
    data_output_proc = Process(target=sm.DataOutputProc, args=(queue_store,))

    # start processes and manager
    url_manager_proc.start()
    result_solve_proc.start()
    data_output_proc.start()
    manager.get_server().serve_forever()

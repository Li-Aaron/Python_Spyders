# -*- coding: utf-8 -*-
'''
multiprocessing workers
分布式进程
@Author: AC
2017-10-15
CPU密集型操作：多进程(multiprocessing)，使用多核
IO密集型操作：多线程(threading)，使用单核，有GIL全局解释器锁
分布式进程：分布到多台机器上实现，通过网络通信进行管理
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import os, time, random
from multiprocessing.managers import BaseManager
##############################################
#------------------常量定义------------------#
##############################################

##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################

###################################
# QueueManager
# =BaseManager
###################################
class QueueManager(BaseManager):
    pass

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # 主线程
    # register方法将队列获取注册名
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')

    # 连接服务器
    server_addr = '127.0.0.1'
    print 'Connect to server %s ...' % server_addr

    # 验证口令，端口
    m = QueueManager(address=(server_addr, 8001),authkey='AC')

    # 从网络链接
    m.connect()

    # 获取Queue对象
    task = m.get_task_queue()
    result = m.get_result_queue()

    # 从task队列获取任务，并把结果写入result队列
    while(not task.empty()):
        image_url = task.get(True, timeout=5)
        print 'run task download %s ...' % image_url
        time.sleep(1)
        result.put('%s---->success'%image_url)

    # 处理结果
    print('worker exit.')






# -*- coding: utf-8 -*-
'''
multiprocessing managers
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
import Queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support
##############################################
#------------------常量定义------------------#
##############################################
task_number = 100
urls = ["ImageUrl_"+str(i) for i in range(task_number)]
task_queue = Queue.Queue(task_number)      # 任务队列
result_queue = Queue.Queue(task_number)    # 结果队列

##############################################
#------------------函数定义------------------#
##############################################
def get_task():
    return task_queue
def get_result():
    return result_queue

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
    # windows下多进程可能会有问题，添加这句可以缓解
    freeze_support()

    # register方法将队列注册在网络上
    QueueManager.register('get_task_queue', callable=get_task)
    QueueManager.register('get_result_queue', callable=get_result)

    # 绑定端口8001，注册密码
    manager = QueueManager(address=('127.0.0.1', 8001), authkey='AC')

    # 启动服务
    manager.start()
    try:
        # 通过管理实例的方法获得通过网络访问的Queue对象
        task = manager.get_task_queue()
        result = manager.get_result_queue()

        # 添加任务
        for url in urls:
            print 'put task %s ...' % url
            task.put(url)

        # 获取返回结果
        print 'try get result ...'
        for i in range(task_number):
            print 'result is %s' % result.get(timeout=1000)
    except:
        print('Manager error')
    finally:
        # 一定要关闭，否则会爆管道未关闭的错误
        # 关闭进程
        manager.shutdown()
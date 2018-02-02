#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
程序名称 MultiTelnetMaster
@Author: AC
2018-2-2
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
##############################################
import os,time,sys
from multiprocessing import Queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support
from telnetlib import Telnet

##############################################
#------------------常量定义------------------#
##############################################
MAX_QUEUE_LEN = 100
queue_from_slave = Queue(MAX_QUEUE_LEN)      # slave -> master
queue_to_slave = Queue(MAX_QUEUE_LEN)      # master -> slave

MANAGER_IP = '127.0.0.1'
MANAGER_PORT = 8001
TELNET_IP = '127.0.0.1'
TELNET_PORT = 23
##############################################
#------------------函数定义------------------#
##############################################
def get_queue_from_slave():
    return queue_from_slave
def get_queue_to_slave():
    return queue_to_slave

##############################################
#------------------类定义--------------------#
##############################################
class QueueManager(BaseManager):
    pass

class TelnetLog(object):
    def __init__(self, filename, logType = 0):
        if not isinstance(logType, int) or not isinstance(filename, basestring):
            raise TypeError('logType = 0 or 1')
        elif logType < 0 or logType > 1:
            raise ValueError('logType = 0 or 1')
        self.filename = filename
        self.logType = logType


    def GetLocalTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

    def LogPrint(self, string):
        if isinstance(string, str):
            string = string.decode().encode('gbk')
        elif isinstance(string, unicode):
            string = string.encode('gbk')
        else:
            raise TypeError('string must be basestring')

        if self.logType > 0:
            sys.stdout.write(string)
        with open(self.filename,'ab+') as f:
            f.writelines('[%s]\n' % self.GetLocalTime())
            f.writelines('%s\n' % string)

class TelnetMaster(Telnet):
    def listener(self, queue_from_slave, queue_to_slave):
        '''
        :param queue_from_slave: slave -> master (input)
        :param queue_to_slave: master -> slave (output)
        :return:
        '''
        logFilename = 'telnetLog_%s.txt' % time.strftime("%Y%m%d_%H%M%S",time.localtime())
        tLogObj = TelnetLog(filename = logFilename, logType = 1)

        while True:
            cmdFlag = False
            try:
                try:
                    # cmd from slave
                    dictFromSlave = queue_from_slave.get(True, timeout = 1)
                    cmdFlag = True
                    cmd = dictFromSlave['cmd']
                    delay = dictFromSlave['delay']
                    self.write(cmd + '\n')
                    time.sleep(delay)
                    data = self.read_very_eager()
                except:
                    # timeout
                    data = self.read_very_eager()
            except EOFError:
                print '*** Connection closed by remote host ***'
                return
            if data:
                if cmdFlag:
                    dictToSlave = {'data': data}
                    queue_to_slave.put(dictToSlave, timeout=1)
                tLogObj.LogPrint(data)
            else:
                sys.stdout.flush()

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    print 'Process MultiTelnetMaster (%s) Running...' % (os.getpid())

    # windows下多进程可能会有问题，添加这句可以缓解
    freeze_support()

    # register方法将队列获取注册名
    QueueManager.register('get_queue_from_slave', callable=get_queue_from_slave)
    QueueManager.register('get_queue_to_slave', callable=get_queue_to_slave)

    # 绑定端口8001，注册密码
    manager = QueueManager(address=(MANAGER_IP, MANAGER_PORT), authkey='AC')

    # 启动服务
    manager.start()

    # 通过管理实例的方法获得通过网络访问的Queue对象
    q_from_slave = manager.get_queue_from_slave()
    q_to_slave = manager.get_queue_to_slave()

    telnetObj = TelnetMaster(host=TELNET_IP, port=TELNET_PORT)
    try:
        telnetObj.listener(q_from_slave, q_to_slave)
    except Exception as e:
        print('*** Manager error ***')
        print e
    finally:
        # 关闭进程
        telnetObj.close()
        manager.shutdown()

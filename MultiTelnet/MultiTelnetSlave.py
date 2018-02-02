#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
程序名称 MultiTelnetSlave
@Author: AC
2018-2-2
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
##############################################
import os,time,sys
from MultiTelnetMaster import QueueManager,TelnetLog

##############################################
#------------------常量定义------------------#
##############################################
MANAGER_IP = '127.0.0.1'
MANAGER_PORT = 8001

##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################

class TelnetSlave(object):
    def __init__(self, queue_from_slave, queue_to_slave):
        self.q_from_slave = queue_from_slave
        self.q_to_slave = queue_to_slave
        logFilename = 'telnetLog_%s.txt' % time.strftime("%Y%m%d_%H%M%S",time.localtime())
        self.tLogObj = TelnetLog(filename = logFilename, logType = 1)

    def WriteToTelnet(self, cmd, delay = 1):
        if not isinstance(cmd, basestring):
            raise TypeError
        dictToMaster = {'cmd':cmd, 'delay':delay}
        self.q_from_slave.put(dictToMaster, timeout=1)
        retryTime = 5
        while retryTime:
            try:
                dictFromMaster = self.q_to_slave.get(True, timeout = delay)
                data = dictFromMaster['data']
                self.tLogObj.LogPrint(data)
                return data
            except:
                retryTime -= 1
        raise IOError('Timeout from master')



##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    print 'Process MultiTelnetSlave (%s) Running...' % (os.getpid())

    # register方法将队列获取注册名
    QueueManager.register('get_queue_from_slave')
    QueueManager.register('get_queue_to_slave')


    manager = QueueManager(address=(MANAGER_IP, MANAGER_PORT),authkey='AC')

    # 从网络链接
    manager.connect()

    # 通过管理实例的方法获得通过网络访问的Queue对象
    q_from_slave = manager.get_queue_from_slave()
    q_to_slave = manager.get_queue_to_slave()

    tsObj = TelnetSlave(q_from_slave, q_to_slave)

    tsObj.WriteToTelnet('ls -al')

# -*- coding: utf-8 -*-
'''
threading Synchronize
@Author: AC
2017-10-15
CPU密集型操作：多进程(multitasking)，使用多核
IO密集型操作：多线程(threading)，使用单核，有GIL全局解释器锁
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import os, time, random
import threading
##############################################
#------------------常量定义------------------#
##############################################
mylock = threading.RLock()
num = 0

##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################

###################################
# myThread
# Thread继承类
################################### 
class myThread(threading.Thread):
	###################################
	# __init__
	# 初始化
	###################################
	def __init__(self,name):
		threading.Thread.__init__(self,name=name)

	###################################
	# run
	# 线程启动
	###################################
	def run(self):
		global num
		while True:
			mylock.acquire()
			print '[Sub] %s locked, Number: %d' % (threading.current_thread().name, num)
			if num >= 4:
				print '[Sub] %s released, Number: %d' % (threading.current_thread().name, num)
				mylock.release()
				break
			num += 1
			print '[Sub] %s released, Number: %d' % (threading.current_thread().name, num)
			mylock.release()

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
	# 主线程
	print '[Main] %s running()...' % threading.current_thread().name
	# 创建threading
	t1 = myThread(name='Thread_1')
	t2 = myThread(name='Thread_2')

	t1.start() # 启动子线程
	t2.start()

	t1.join() # 阻塞主线程（不用join的话主线程会继续运行）
	t2.join()

	print '[Main] %s ended.' % threading.current_thread().name






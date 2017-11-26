# -*- coding: utf-8 -*-
'''
threading BASICS
@Author: AC
2017-10-15
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

##############################################
#------------------函数定义------------------#
##############################################

###################################
# thread_run
# 运行线程
################################### 
def thread_run(urls):
	print '[Sub] %s running()...' % threading.current_thread().name
	for url in urls:
		print '%s ------>>> %s ' % (threading.current_thread().name, url)
		time.sleep(random.random())
	print '[Sub] %s ended.' % threading.current_thread().name


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
	def __init__(self,name,urls):
		threading.Thread.__init__(self,name=name)
		self.urls = urls

	###################################
	# run
	# 线程启动
	###################################
	def run(self):
		print '[Sub] %s running()...' % threading.current_thread().name
		for url in self.urls:
			print '%s ------>>> %s ' % (threading.current_thread().name, url)
			time.sleep(random.random())
		print '[Sub] %s ended.' % threading.current_thread().name


##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
	# 主线程
	print '[Main] %s running()...' % threading.current_thread().name
	# 创建threading
	t1 = myThread(name='Thread_1',urls=['urlA_'+str(i) for i in range(3)])
	t2 = myThread(name='Thread_2',urls=['urlB_'+str(i) for i in range(3)])

	t1.start() # 启动子线程
	t2.start()

	t1.join() # 阻塞主线程（不用join的话主线程会继续运行）
	t2.join()

	print '[Main] %s ended.' % threading.current_thread().name






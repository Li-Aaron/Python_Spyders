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

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
	# 主线程
	print '[Main] %s running()...' % threading.current_thread().name
	# 创建threading
	t1 = threading.Thread(target=thread_run, name='Thread_1',args=(['urlA_'+str(i) for i in range(3)],))
	t2 = threading.Thread(target=thread_run, name='Thread_2',args=(['urlB_'+str(i) for i in range(3)],))

	t1.start() # 启动子线程
	t2.start()

	t1.join() # 阻塞主线程（不用join的话主线程会继续运行）
	t2.join()

	print '[Main] %s ended.' % threading.current_thread().name






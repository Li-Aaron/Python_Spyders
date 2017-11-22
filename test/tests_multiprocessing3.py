# -*- coding: utf-8 -*-
'''
multiprocessing module communication USING QUEUE
@Author: AC
2017-10-15
'''
__author__ = 'AC'

 
import os, time, random
from multiprocessing import Process, Queue
###################################
# 常量定义
###################################
url1 = ['url1_1','url1_2','url1_3',]
url2 = ['url2_1','url2_2','url2_3',]

###################################
# 函数定义
###################################

###################################
# proc_write
# 向进程里写
################################### 
def proc_write(q, urls):
	print 'Process (%s) Running(Writing)...' % (os.getpid())
	for url in urls:
		q.put(url, True)
		print 'Put %s to queue...' % url
		time.sleep(random.random())
	print 'Process (%s) Done(Writing)...' % (os.getpid())

###################################
# proc_read
# 从进程里读
################################### 
def proc_read(q):
	print 'Process (%s) Running(Reading)...' % (os.getpid())
	while True:
		url = q.get(True)
		print 'Get %s from queue...' % url
		time.sleep(random.random())


###################################
# 脚本开始
###################################
if __name__ == '__main__':
	# 父进程创建Queue，并传输给各个子进程：
	q = Queue()
	proc_writer1 = Process(target = proc_write, args = (q, url1))
	proc_writer2 = Process(target = proc_write, args = (q, url2))
	proc_reader1 = Process(target = proc_read, args = (q, ))

	proc_writer1.start() # 启动子线程
	proc_writer2.start()
	proc_reader1.start()

	proc_writer1.join() # 阻塞主线程（不用join的话主线程会继续运行）
	
	proc_writer2.join()

	time.sleep(5)
	proc_reader1.terminate() # 死循环只能强行终止




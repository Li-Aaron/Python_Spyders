# -*- coding: utf-8 -*-
'''
multiprocessing module communication USING PIPE
@Author: AC
2017-10-15
'''
__author__ = 'AC'

 
import os, time, random
import multiprocessing
###################################
# 常量定义
###################################
url1 = ['url1_1','url1_2','url1_3',]
url2 = ['url2_1','url2_2','url2_3',]

###################################
# 函数定义
###################################

###################################
# proc_send
# 向PIPE里发送
################################### 
def proc_send(pipe, urls):
	print 'Process (%s) Running(Writing)...' % (os.getpid())
	for url in urls:
		print 'Process (%s) send %s to pipe...' % (os.getpid(),url)
		pipe.send(url)
		time.sleep(random.random())
	print 'Process (%s) Done(Writing)...' % (os.getpid())

###################################
# proc_recv
# 从PIPE里读
################################### 
def proc_recv(pipe):
	print 'Process (%s) Running(Reading)...' % (os.getpid())
	while True:
		url = pipe.recv()
		print 'Process (%s) recv %s from pipe...' % (os.getpid(),url)
		time.sleep(random.random())


###################################
# 脚本开始
###################################
if __name__ == '__main__':
	# 父进程创建Queue，并传输给各个子进程：
	pipe = multiprocessing.Pipe()
	p1 = multiprocessing.Process(target = proc_send, args = (pipe[0], ['url_'+str(i) for i in range(10)]))
	p2 = multiprocessing.Process(target = proc_recv, args = (pipe[1],))


	p1.start() # 启动子线程
	p2.start()

	p1.join() # 阻塞主线程（不用join的话主线程会继续运行）
	p2.terminate()





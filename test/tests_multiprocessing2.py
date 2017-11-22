# -*- coding: utf-8 -*-
'''
@Author: AC
2017-10-15
'''
__author__ = 'AC'

# multiprocessing module
import os, time, random
from multiprocessing import Pool

# 被调用的函数
def run_proc(name):
	print 'Child process %s (%s) Running...' % (name, os.getpid())
	sleeptime = random.random()*3
	print 'Sleep '+str(sleeptime)+' seconds'
	time.sleep(sleeptime)
	print 'Task %s end.' % name

if __name__ == '__main__':
	print 'Parent process %s.' % os.getpid()
	p = Pool(processes = 3) # 进程池管理，最大进程=3
	for i in range(5):
		p.apply_async(run_proc, args = (str(i),))
		# p = Process(target=run_proc, args=(str(i),)) # 建立函数线程，名称和参数
	print 'Waiting for all subprocesses done...'
	p.close() 
	p.join() # join之前必须close,close之后不能在Pool中添加新进程
	print 'All subprocess done.'



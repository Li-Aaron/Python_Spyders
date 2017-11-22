# -*- coding: utf-8 -*-
'''
@Author: AC
2017-10-15
'''
__author__ = 'AC'

# multiprocessing module
import os
from multiprocessing import Process

# 被调用的函数
def run_proc(name):
	print 'Child process %s (%s) Running...' % (name, os.getpid())
	a = 0
	for i in range(10000000):
		a = a + i
	print a

if __name__ == '__main__':
	print 'Parent process %s.' % os.getpid()
	for i in range(5):
		p = Process(target=run_proc, args=(str(i),)) # 建立函数线程，名称和参数
		print 'Process will start.'
		p.start() # 启动线程
	p.join()
	print 'Process end.'



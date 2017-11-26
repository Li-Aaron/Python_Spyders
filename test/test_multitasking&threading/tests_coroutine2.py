# -*- coding: utf-8 -*-
'''
threading coroutine(协程、微线程) Pool
@Author: AC
2017-10-15
CPU密集型操作：多进程(multiprocessing)，使用多核
IO密集型操作：多线程(threading)，使用单核，有GIL全局解释器锁
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import os, time, random
from gevent import monkey; monkey.patch_all
import gevent
from gevent.pool import Pool
import urllib2
##############################################
#------------------常量定义------------------#
##############################################
urls = ["https://github.com/",
		"https://www.python.org/",
		"https://www.cnblogs.com/" 
		]

##############################################
#------------------函数定义------------------#
##############################################

###################################
# run_task
# 执行task
###################################
def run_task(url):
	print 'Visit --> %s' % url
	try:
		response = urllib2.urlopen(url)
		data = response.read()
		print '%d bytes received from %s.' % (len(data), url)
	except Exception,e:
		print e
	return 'url:%s ---> finish' % url


##############################################
#------------------类定义--------------------#
##############################################


##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
	pool = Pool(2)
	results = pool.map(run_task, urls)
	print results
	# greenlets = [gevent.spawn(run_task, url) for url in urls]
	# gevent.joinall(greenlets)






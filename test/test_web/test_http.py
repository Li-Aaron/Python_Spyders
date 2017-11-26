# -*- coding: utf-8 -*-
'''
程序名称
@Author: AC
2017-11-26
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import urllib2,urllib
import cookielib
import socket

##############################################
#------------------常量定义------------------#
##############################################

##############################################
#------------------函数定义------------------#
##############################################

###################################
# function
# 函数
################################### 

##############################################
#------------------类定义--------------------#
##############################################

###################################
# class
# 类
################################### 

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # 主线程
    url = "http://www.quyuege.com/xs/43/43176/"
    user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
    referer = "http://www.quyuege.com/"

    socket.setdefaulttimeout(10)
    urllib2.socket.setdefaulttimeout(10)

    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request, timeout=5)
        print response.getcode()
        # html = response.read()
        # print html
    except urllib2.HTTPError as e:
        if hasattr(e, 'code'):
            print 'Error Code: %s' % e.code
        request.add_header('User-Agent',user_agent)
        request.add_header('Referer',referer)
        response = urllib2.urlopen(request, timeout=5)
        html = response.read()
        print response.getcode()
        # print html


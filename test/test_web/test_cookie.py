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
    url = "http://www.baidu.com"
    # GET 1
    response = urllib2.urlopen(url)
    html = response.read()
    #print html


    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(url)
    for item in cookie:
        print "%s: %s" % (item.name, item.value)
    print ""

    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'email=' + 'xxx@163.com'))
    req = urllib2.Request(url)
    response = opener.open(req)
    print response.headers
    retdata = response.read()
    print ""
    # print retdata
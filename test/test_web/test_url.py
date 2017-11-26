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

    # GET 1
    response = urllib2.urlopen("http://www.baidu.com")
    html = response.read()
    # print html

    # GET 2
    request = urllib2.Request("http://www.baidu.com")
    response = urllib2.urlopen(request)
    html = response.read()
    # print html

    # POST
    url = "https://passport.cnblogs.com/user/signin"
    user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
    referer = "https://www.cnblogs.com/"
    postdata = {'username':'xxx',
                'password':'xxx'}
    data = urllib.urlencode(postdata)
    req = urllib2.Request(url)
    req.add_header('User-Agent',user_agent)
    req.add_header('Referer',referer)
    req.add_data(data)
    response = urllib2.urlopen(req)
    html = response.read()
    print html

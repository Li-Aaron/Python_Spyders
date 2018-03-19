#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
程序名称
@Author: AC
2018-3-18
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import DesiredCapabilities
import time

##############################################
#------------------常量定义------------------#
##############################################
url = "http://www.baidu.com/"
##############################################
#------------------函数定义------------------#
##############################################

##############################################
#------------------类定义--------------------#
##############################################

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # 主线程
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) "
                                                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36")
    driver = webdriver.PhantomJS()
    driver.get(url)
    time.sleep(1)

    assert u"百度" in driver.title
    elem = driver.find_element_by_name("wd")
    elem.clear()
    elem.send_keys(u"网络爬虫")
    elem.send_keys(Keys.RETURN)
    time.sleep(3)
    assert u"网络爬虫." not in driver.page_source
    print driver.find_element_by_id("1").text
    driver.close()


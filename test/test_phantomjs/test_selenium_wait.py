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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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
    # driver.implicitly_wait(1) # 隐式等待
    driver.get(url)
    time.sleep(1)

    assert u"百度" in driver.title
    elem = driver.find_element_by_name("wd")
    elem.clear()
    elem.send_keys(u"网络爬虫")
    elem.send_keys(Keys.RETURN)
    try:
        # 显式等待
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "1"))
        )
        print elem.text
    finally:
        driver.close()


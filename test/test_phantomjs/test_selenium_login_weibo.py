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
import time
##############################################
#------------------常量定义------------------#
##############################################
url = "https://login.sina.com.cn/signup/signin.php"
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
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(1)
    # username = driver.find_element_by_id('username')
    # password = driver.find_element_by_id('password')
    username = driver.find_element_by_xpath('.//*[@id="username"]')
    password = driver.find_element_by_xpath('.//*[@id="password"]')
    login_button = driver.find_element_by_xpath('//input[@type="submit"]')

    username.send_keys("*********")
    password.send_keys("*********")
    login_button.click()

    time.sleep(2)
    # url = 'https://weibo.com/p/1005052259181527/info'
    # driver.get(url)
    # time.sleep(2)
    print driver.page_source


    driver.close()
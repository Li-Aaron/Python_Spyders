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
url = "file:///D:/Codes/Python/Python_Spyders/test/test_phantomjs/login.html"
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
    username = driver.find_element_by_name('username')
    password = driver.find_element_by_xpath('.//*[@id="loginForm"]/input[2]')
    login_button = driver.find_element_by_xpath('//input[@type="submit"]')

    username.send_keys("ac")
    password.send_keys("ac_pass")
    # login_button.click()

    time.sleep(1)
    username.clear()
    password.clear()

    # this is not a good way
    time.sleep(1)
    select = driver.find_element_by_xpath("//form/select")
    # 注意是elements
    all_options = select.find_elements_by_tag_name("option")
    for option in all_options:
        print "Value is : %s" % option.get_attribute("value")
        option.click()

    # official way
    from selenium.webdriver.support.ui import Select
    select = Select(driver.find_element_by_xpath('//form/select'))
    select.select_by_index(0)
    time.sleep(1)
    select.select_by_visible_text("手机号")
    time.sleep(1)
    select.select_by_value("name")
    time.sleep(1)

    driver.close()
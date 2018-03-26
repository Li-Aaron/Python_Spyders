#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
程序名称
@Author: AC
2018-3-21
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
##############################################
import requests
from bs4 import BeautifulSoup

##############################################
#------------------常量定义------------------#
##############################################
# agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.0'
headers = {
    'User-Agent': agent,
}
username = 'lsp_python@yeah.net'
password = '139849e7b513a738'
##############################################
#------------------函数定义------------------#
##############################################
def get_authenticity_token(session):
    '''
    <meta content="authenticity_token" name="csrf-param" />
    <meta content="UTQf3UZni9YJ8AuViCC86WD8jkqD4fiSIHElvpIaX84=" name="csrf-token" />
    get token
    '''
    url = 'https://gitee.com/login'
    index_page = session.get(url, headers=headers)
    html_content = index_page.text
    soup = BeautifulSoup(html_content,'html.parser')
    # name 是find的定参，不能直接带入，需要建立attr
    token = soup.find('meta', attrs={'name':'csrf-token'})['content']
    return token

def isLogin(session):
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://gitee.com/profile"
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False
##############################################
#------------------类定义--------------------#
##############################################

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # 主线程
    session = requests.session()
    token = get_authenticity_token(session)
    print(token)

    postdata = {
        'authenticity_token' : token,
        'captcha' : None,
        'commit' : '登 录',
        'redirect_to_url' : None,
        'user[login]' : username,
        'user[password]' : password,
        'user[remember_me]' : 0,
        'utf8' : '✓',
    }
    login_url = 'https://gitee.com/login'
    login_page = session.post(login_url, data=postdata, headers=headers)
    # print(login_page.text)
    print(login_page.status_code)
    print(isLogin(session))





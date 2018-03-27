#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
qiyeboy 的 IPProxyPool HTTP get 获取
@Author: AC
2018-3-27
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import requests
import json
from bs4 import BeautifulSoup

from Common import logger
##############################################
#------------------常量定义------------------#
##############################################

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
    ip_count = 10
    url = 'http://127.0.0.1:8000/?types=0&count=%s'%ip_count
    r = requests.get(url, timeout=5)
    ip_pool = json.loads(r.text)
    ip_useful = []
    for ip_port in ip_pool:
        ip = ip_port[0]
        port = ip_port[1]
        logger.info("ip = %s, port = %s"%(ip,port))
        proxies = {
            'http':'http://%s:%s'%(ip,port),
            'https':'https://%s:%s'%(ip,port),
        }
        try:
            r = requests.get('http://ip.chinaz.com/',proxies=proxies,timeout=5)
            r.encoding='utf-8'
            soup = BeautifulSoup(r.text,"lxml")
            ip_chinaz = soup.find('p',class_='getlist').text
            logger.info('%s connect success' % ip)
            logger.info(ip_chinaz)
            ip_useful.append(ip_port)
        except Exception:
            logger.warn('%s connect failed' % ip)
    logger.info(ip_useful)
    logger.info('useful ip : %d'%len(ip_useful))



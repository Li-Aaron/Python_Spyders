# -*- coding: utf-8 -*-
'''
程序名称 Common
一般方法
@Author: AC
2018-3-12
'''
__author__ = 'AC'

##############################################
#------------------logging-------------------#
##############################################
import logging.config, yaml
log_conf = './logger.yml'
with open(log_conf, 'rt') as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)
logger = logging.getLogger('manager')

##############################################
#------------------函数定义------------------#
##############################################
def Schedule(num, totalNum, printFlg = True, note = ''):
    process = 100.0 * num / totalNum
    note = '(%s)'% note if note else ''
    if printFlg:
        logger.warn("[%4.3f%%] %5d of %5d is done %s..." % (process, num, totalNum, note))
    return process

#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
logger
@Author: AC
2017-11-5
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
##############################################
import functools
import traceback
##############################################
#------------------logging-------------------#
##############################################
import logging.config, yaml
log_conf = './logger.yml'
with open(log_conf, 'rt') as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)
logger = logging.getLogger('master')
logger_manager = logging.getLogger('manager')
logger_node = logging.getLogger('node')
##############################################
#------------------函数定义------------------#
##############################################
def log(level = logging.INFO):
    '''
    decorator to save log of a function (entrance)
    :param level:  logging_levelNames.keys()
    :return:
    '''
    LEVEL = logging._levelNames.keys()
    if level not in LEVEL:
        raise ValueError('No Such Level')
    if not isinstance(level, int):
        level = logging.getLevelName(level)
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            string = '%s(%s, %s)' % (func.__name__, args, kwargs)
            logger.log(level, string)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(e)
                logger.error('%s\n%s\n' % (func.__name__, traceback.format_exc()))
                # raise e
        return wrapper
    return decorator

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    @log()
    def fun1(a, b = '1'):
        print(a,b)

    @log(40)
    def fun2(a, b = '1'):
        print(a,b)

    @log('WARN')
    def fun3(a, b = '1'):
        print(a,b)

    @log(logging.ERROR)
    def fun4(a, b = '1'):
        print(a,b)

    fun1(1,'2')
    fun2(1,'3')
    fun3(1,'4')
    fun4(1,'5')
    fun1(1)
    fun1()
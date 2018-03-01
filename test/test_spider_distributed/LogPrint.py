# -*- coding: utf-8 -*-
'''
程序名称 LogPrint
@Author: AC
2018-2-26
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import time
import chardet

##############################################
#------------------常量定义------------------#
##############################################
INFO = 0x1
ERROR = 0x2
DEBUG = 0x4
DISP = 0x10
FILE = 0x20

TYPE_DICT = {INFO:'INFO',ERROR:'ERROR',DEBUG:'DEBUG'}

CONTROL = INFO|ERROR|DEBUG|DISP|FILE
##############################################
#------------------函数定义------------------#
##############################################
def ToUTF8(content):
    if isinstance(content, unicode):
        return content.encode('utf-8')
    else:
        return content.decode(chardet.detect(content)['encoding']).encode('utf-8')


def LogPrint(content, log_type = INFO, log_control = CONTROL, filename = 'log.txt'):
    if log_type not in TYPE_DICT.keys():
        log_type = INFO
    if log_type & log_control:
        format_str = '[%s]%s' %(TYPE_DICT[log_type], content)
        if log_control & DISP:
            print format_str
        if log_control & FILE:
            with open(filename, 'ab+') as fout:
                fout.write('[%s]%s\n'%(time.strftime("%Y%m%d_%H%M%S",time.localtime()),format_str))


##############################################
#------------------类定义--------------------#
##############################################

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    content = 'Test Print'
    LogPrint(content)
    LogPrint(content, log_type=INFO)
    LogPrint(content, log_type=ERROR)
    LogPrint(content, log_type=DEBUG)
    CONTROL = INFO | ERROR
    LogPrint(content)
    LogPrint(content, log_type=INFO)
    LogPrint(content, log_type=ERROR)
    LogPrint(content, log_type=DEBUG)
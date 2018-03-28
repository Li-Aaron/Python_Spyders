# -*- coding: utf-8 -*-
'''
程序名称 Common
一般方法
@Author: AC
2018-3-12
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
##############################################
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from logger import logger


##############################################
#------------------函数定义------------------#
##############################################
def Schedule(num, totalNum, printFlg = True, note = ''):
    process = 100.0 * num / totalNum
    note = '(%s)'% note if note else ''
    if printFlg:
        logger.warn("[%4.3f%%] %5d of %5d is done %s..." % (process, num, totalNum, note))
    return process

def OpenImg(path):
    img = mpimg.imread(path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()
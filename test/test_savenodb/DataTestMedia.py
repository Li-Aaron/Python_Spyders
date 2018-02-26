# -*- coding: utf-8 -*-
'''
程序名称 DataTestMedia
@Author: AC
2018-2-25
'''
__author__ = 'AC'

##############################################
# ------------------import--------------------#
##############################################
import WebCommon
import urllib
from lxml import etree


##############################################
# ------------------常量定义------------------#
##############################################
URL = 'http://www.ivsky.com/tupian/ziranfengguang/'
EOL = u'\n'

##############################################
# ------------------函数定义------------------#
##############################################
def Schedule(blocknum, blocksize, totalsize):
    '''
    reporthook(blocknum, bs, size)
    :param blocknum: downloaded blocks
    :param blocksize: block size
    :param totalsize: file size
    :return:
    '''
    per = 100.0 * blocknum * blocksize / totalsize
    if per > 100:
        per = 100
    print 'Downloading: %04.2f' % per

##############################################
# ------------------类定义--------------------#
##############################################


##############################################
# ------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    wc = WebCommon.WebCommon(URL)
    html = wc.OpenWebPageReq()

    html_et = etree.HTML(html)
    img_urls = html_et.xpath('.//img/@src')
    idx = 0
    for img_url in img_urls:
        filename = 'img%03d.jpg' % (idx,)
        print filename
        urllib.urlretrieve(img_url, filename, Schedule)
        idx += 1
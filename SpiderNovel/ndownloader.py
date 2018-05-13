# -*- coding: utf-8 -*-
'''
程序名称 NovelGeDownloader--www.23us.la
@Author: AC
2017-12-25
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import re
import sys
from SpiNovel import NovelDownloader_QuYueGe
from SpiNovel import NovelDownloader_Biquwu
from SpiNovel import NovelDownloader_23us
from SpiNovel import NovelDownloader_Yixuanju


##############################################
#------------------常量定义------------------#
##############################################
# URL = 'http://www.quyuege.com/xs/43/43176/'
# URL = 'https://www.23us.la/html/247/247068/'
# URL = 'http://www.ucxiaoshuo.com/book/9354/'
URL = 'http://www.yixuanju.com/book/16111'
EOL = u'\n'

##############################################
#------------------函数定义------------------#
##############################################
def downloader_selector(url):
    pattern = re.compile(r'//www\.(.*?)\.')
    matchObj = pattern.search(url)
    if matchObj:
        if matchObj.group(1) == '23us':
            return NovelDownloader_23us(url)
        elif matchObj.group(1) == 'quyuege':
            return NovelDownloader_QuYueGe(url)
        elif matchObj.group(1) == 'ucxiaoshuo':
            return NovelDownloader_Biquwu(url)
        elif matchObj.group(1) == 'yixuanju':
            return NovelDownloader_Yixuanju(url)
        else:
            raise Exception('No valid downloader for %s'%matchObj.group(1))
    else:
        raise Exception('Not valid url: %s'%url)


##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    webPageUrl = URL
    startChap = 1
    if len(sys.argv) < 2:
        print 'For debug usage!'
    elif len(sys.argv) == 2:
        webPageUrl = str(sys.argv[1])
    elif len(sys.argv) == 3:
        webPageUrl = str(sys.argv[1])
        startChap = int(sys.argv[2])
    else:
        raise Exception("too many input parameters (>2)")

    if startChap < 1:
        raise ValueError("startChap must larger than 1")

    novelDL = downloader_selector(webPageUrl)
    novelDL.GetNovel(startChap)

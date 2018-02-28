# -*- coding: utf-8 -*-
'''
程序名称 HtmlDownloader
下载网页
@Author: AC
2018-2-26
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import requests

##############################################
#------------------常量定义------------------#
##############################################


##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################
class HtmlDownloader(object):

    user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"

    def OpenWebPage(self, url):
        headers = {'User-Agent':self.user_agent}
        html = ''
        timeoutCount = 5
        while not html:
            try:
                req = requests.get(url, headers=headers, timeout=20)
                if req.status_code == 200:
                    req.encoding = 'utf-8'
                    html = req.text
                    return html
                else:
                    return None
            except requests.Timeout:
                if not timeoutCount:
                    return None
                print '[Error] Time out retry %s' % url
                timeoutCount -= 1


##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    pass


# -*- coding: utf-8 -*-
'''
程序名称 UrlManager
URL管理器，管理URL用
@Author: AC
2018-2-26
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 


##############################################
#------------------常量定义------------------#
##############################################


##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################
class UrlManager(object):
    def __init__(self):
        # 用集合是避免重复url
        self.new_urls = set() # url not crawled
        self.old_urls = set() # url crawled

    def HasNewUrl(self):
        '''
        if there are new_urls
        :return:
        '''
        return self.NewUrlSize() != 0

    def GetNewUrl(self):
        '''
        get a uncrawled url
        :return:
        '''
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def AddNewUrl(self, url):
        '''
        put a new url to new_urls
        :param url: single url
        :return:
        '''
        if not isinstance(url, (str, unicode)):
            raise TypeError('input url must be string/unicode not %s'%type(url))
        url = url.decode('utf-8') if isinstance(url, str) else url
        self.new_urls.add(url)

    def AddNewUrls(self, urls):
        '''
        put new url set to new_urls
        :param url: single url
        :return:
        '''
        if not isinstance(urls, set):
            raise TypeError('input urls must be set not %s'%type(urls))
        for url in urls:
            if url not in self.old_urls:
                self.new_urls.add(url)

    def NewUrlSize(self):
        '''
        return size of new_urls
        :return:
        '''
        return len(self.new_urls)

    def OldUrlSize(self):
        '''
        return size of old_urls
        :return:
        '''
        return len(self.old_urls)

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    pass


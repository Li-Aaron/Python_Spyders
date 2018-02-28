# -*- coding: utf-8 -*-
'''
程序名称 UrlManager - Distributed
URL管理器，管理URL用
@Author: AC
2018-2-28
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
try:
    import cPickle as pickle
except ImportError:
    import pickle
import hashlib

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
        get a uncrawled url/ save old url with md5 process
        :return:
        '''
        new_url = self.new_urls.pop()
        m = hashlib.md5()
        m.update(new_url.encode('utf-8'))
        self.old_urls.add(m.hexdigest()[8:-8]) # 只保存中间128bit
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
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
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
            self.AddNewUrl(url)

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

    def SaveProgress(self, data, filename = 'progress.txt'):
        '''
        progress pickle to filename
        :param filename:
        :param data:
        :return:
        '''
        with open(filename, 'wb') as fout:
            pickle.dump(data, fout)

    def LoadProgress(self, filename = 'progress.txt'):
        '''
        progress load from filename
        :param filename:
        :return: set of data
        '''
        try:
            with open(filename, 'rb') as fin:
                data = pickle.load(fin)
        except:
            print 'no progress file %s' % (filename,)
            data = set()
        return data


##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    pass


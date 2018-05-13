# -*- coding: utf-8 -*-
'''
程序名称 NovelGeDownloader--www.yixuanju.com
@Author: AC
20118-5-13
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
##############################################
import re
import sys
from SpiNovel import NovelDownloaderGev

##############################################
#------------------常量定义------------------#
##############################################
URL = 'http://www.yixuanju.com/book/16111'
EOL = u'\n'

##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################
class NovelDownloader_Yixuanju(NovelDownloaderGev):

    rootUrl = 'http://www.yixuanju.com'

    def GetNovelListDispatch(self, soup):
        '''
        Get Novel List (BiQuWu Version)
        :param soup: soup of html string lxml
        :return: novel : key('Title','Author','Abstract','UrlList')
        '''
        novel = {}
        novelUrlList = []
        # novel title and properties
        novelProperties = soup.find_all('header', class_="book-info-main")[0]
        novel['Title'] = novelProperties.find_all('h2')[0].string
        novel['Author'] = novelProperties.find_all('div')[0].string
        novelProperties = soup.find_all('div', class_="am-u-sm-9")[0]
        novel['Abstract'] = novelProperties.find_all('div')[0].string

        # novel url list
        novelList = soup.find_all('ul', "am-list am-list-static")[0]
        for novelUrl in novelList.find_all('a'):
            novelUrlList.append(novelUrl['href'])
        novel['UrlList'] = novelUrlList
        return novel

    def GetNovelTextDispatch(self, soup):
        '''
        Get Novel Text (BiQuWu Version)
        :param soup: soup of html string lxml
        :return: title, text
        '''
        # find novel title
        bookContent = soup.find_all('header', class_="am-banner")[0]
        title = bookContent.find_all('h1')[0].string

        # find novel text
        novelText = soup.find_all('article', id="cha-content")[0]
        text = novelText.text

        return title, text



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

    novelDL = NovelDownloader_Yixuanju(webPageUrl)
    novelDL.GetNovel(startChap)

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
import urllib2
from bs4 import BeautifulSoup
import re
import sys
from NovelDownloader import NovelDownloader
from NovelDownloaderMulti import NovelDownloaderMulti
from NovelDownloaderGev import NovelDownloaderGev

##############################################
#------------------常量定义------------------#
##############################################
# URL = 'http://www.quyuege.com/xs/43/43176/'
URL = 'https://www.23us.la/html/247/247068/'
# URL = 'https://www.23us.la/html/151/151769/'
EOL = u'\n'

##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################
class NovelDownloader23us(NovelDownloader):

    rootUrl = 'https://www.23us.la'

    def GetNovelListDispatch(self, soup):
        '''
        Get Novel List (QuYueGe Version)
        :param soup: soup of html string lxml
        :return: novel : key('Title','Author','Abstract','UrlList')
        '''
        novel = {}
        novelUrlList = []
        # novel title and properties
        novelProperties = soup.find_all('div', class_="btitle")[0]
        novel['Title'] = novelProperties.find_all('h1')[0].string
        novel['Author'] = novelProperties.find_all('em')[0].string
        novelProperties = soup.find_all('p', class_="intro")[0]
        novel['Abstract'] = novelProperties.find_all('b')[0].string

        # novel url list
        novelList = soup.find_all('dl', class_="chapterlist")[0]
        for novelUrl in novelList.find_all('a'):
            novelUrlList.append(novelUrl['href'])
        novel['UrlList'] = novelUrlList
        return novel

    def GetNovelTextDispatch(self, soup):
        '''
        Get Novel Text (QuYueGe Version)
        :param soup: soup of html string lxml
        :return: title, text
        '''
        # find novel title
        novelTitle = soup.find_all('div', class_="inner", id="BookCon")[0]
        title = novelTitle.find_all('h1')[0].string
        # find novel text
        matchObj = re.search(u'<div id="content".*?>\s*(.*?)</div>', unicode(novelTitle), re.M | re.S)
        if not matchObj:
            text = ''
        else:
            text = matchObj.group(1)
        return title, text

    def NovelUrlComb(self, novelUrl):
        return self.rootUrl + novelUrl

class NovelDownloader23usMulti(NovelDownloaderMulti,NovelDownloader23us):
    pass

class NovelDownloader23usGev(NovelDownloaderGev,NovelDownloader23us):
    pass


##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    webPageUrl = URL
    startChap = 0
    if len(sys.argv) < 2:
        print 'For debug usage!'
    elif len(sys.argv) == 2:
        webPageUrl = str(sys.argv[1])
    elif len(sys.argv) == 3:
        webPageUrl = str(sys.argv[1])
        startChap = int(sys.argv[2]) - 1
    else:
        raise Exception("too many input parameters (>2)")

    # novelDL = NovelDownloader23us(webPageUrl)
    novelDL = NovelDownloader23usGev(webPageUrl)
    novelDL.GetNovel(startChap)

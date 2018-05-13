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
from SpiNovel import NovelDownloaderGev

##############################################
#------------------常量定义------------------#
##############################################
URL = 'https://www.23us.la/html/247/247068/'
EOL = u'\n'

##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################
class NovelDownloader_23us(NovelDownloaderGev):

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
        urlpattern = re.compile(r'/html/')
        for novelUrl in novelList.find_all('a'):
            if urlpattern.search(novelUrl['href']):
                novelUrlList.append(novelUrl['href'])
        novel['UrlList'] = novelUrlList
        print len(novelUrlList)
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

    novelDL = NovelDownloader_23us(webPageUrl)
    novelDL.GetNovel(startChap)

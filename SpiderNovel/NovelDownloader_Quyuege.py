# -*- coding: utf-8 -*-
'''
程序名称 NovelGeDownloader--www.quyuege.com
@Author: AC
2017-12-30
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
##############################################
import re
import sys
from SpiNovel import NovelDownloader, NovelDownloaderMulti, NovelDownloaderGev

##############################################
#------------------常量定义------------------#
##############################################
URL = 'http://www.quyuege.com/xs/144/144341/'
EOL = u'\n'

##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################
class NovelDownloader_QuYueGe(NovelDownloader):

    def GetNovelListDispatch(self, soup):
        '''
        Get Novel List (QuYueGe Version)
        :param soup: soup of html string lxml
        :return: novel : key('Title','Author','Abstract','UrlList')
        '''
        novel = {}
        novelUrlList = []
        # novel title and properties
        novelProperties = soup.find_all('div', class_="rtext")[0]
        novel['Title'] = novelProperties.find_all('h1')[0].string
        novel['Author'] = novelProperties.find_all('a')[0].string
        novel['Abstract'] = novelProperties.find_all('div', class_="desc")[0].string

        # novel url list
        novelList = soup.find_all('div', "mod mod-article-list")[0]
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
        title = soup.find_all('h1')[0].string

        # find novel text
        novelText = soup.find_all('div', class_="page-content")[0]
        matchObj = re.search(u'固定结束-->(.*)</div>', unicode(novelText), re.M | re.S)
        if not matchObj:
            text = ''
        else:
            text = matchObj.group(1)

        return title, text

    def NovelUrlComb(self, novelUrl):
        return self.webPageUrl + novelUrl

class NovelDownloader_QuYueGeMulti(NovelDownloaderMulti,NovelDownloader_QuYueGe):
    pass

class NovelDownloader_QuYueGeGev(NovelDownloaderGev,NovelDownloader_QuYueGe):
    pass


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

    novelDL = NovelDownloader_QuYueGeGev(webPageUrl)
    novelDL.GetNovel(startChap)

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
URL = 'http://www.ucxiaoshuo.com/book/9354/'
EOL = u'\n'

##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################
class NovelDownloader_Biquwu(NovelDownloader):

    rootUrl = 'http://www.ucxiaoshuo.com'

    def GetNovelListDispatch(self, soup):
        '''
        Get Novel List (QuYueGe Version)
        :param soup: soup of html string lxml
        :return: novel : key('Title','Author','Abstract','UrlList')
        '''
        novel = {}
        novelUrlList = []
        # novel title and properties
        novelProperties = soup.find_all('div', class_="info")[0]
        novel['Title'] = novelProperties.find_all('h1')[0].string
        novel['Author'] = novelProperties.find_all('a')[0].string
        novelProperties = soup.find_all('div', id="intro")[0]
        novel['Abstract'] = novelProperties.find_all('p')[0].string

        # novel url list
        novelList = soup.find_all('div', "article_texttitleb")[0]
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
        bookContent = soup.find_all('div', class_="book_content_text")[0]
        title = bookContent.find_all('h1')[0].string

        # find novel text
        novelText = bookContent.find_all('div', id="book_text")[0]
        text = re.sub(u'<div id="book_text">', u'', unicode(novelText), re.M | re.S)
        text = re.sub(u'</div>', u'', text, re.M | re.S)

        return title, text

    def NovelUrlComb(self, novelUrl):
        return self.rootUrl + novelUrl

class NovelDownloader_BiquwuMulti(NovelDownloaderMulti,NovelDownloader_Biquwu):
    pass

class NovelDownloader_BiquwuGev(NovelDownloaderGev,NovelDownloader_Biquwu):
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

    novelDL = NovelDownloader_BiquwuGev(webPageUrl)
    novelDL.GetNovel(startChap)

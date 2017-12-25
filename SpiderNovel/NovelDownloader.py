# -*- coding: utf-8 -*-
'''
程序名称 NovelDownloader
@Author: AC
2017-12-8
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import urllib2
from bs4 import BeautifulSoup
import re
import sys

##############################################
#------------------常量定义------------------#
##############################################
# URL = 'http://www.quyuege.com/xs/43/43176/'
URL = 'http://www.quyuege.com/xs/144/144341/'
EOL = u'\n'

##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################
class NovelDownloader(object):

    novel = {}
    fileName = 'Novel.txt'

    def __init__(self, url):
        if not isinstance(url, (str)):
            raise TypeError('url mast be string')
        self.webPageUrl = url
        self.novelListHtml = self.OpenWebPage(self.webPageUrl)

    def OpenWebPage(self, url):
        '''
        Open a Webpage and return the html string
        :param url: URL of WebSite
        :return: HTML PAGES
        '''
        user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        html = response.read()
        return html

    def SaveToFile(self, filename, text, attr='w'):
        '''
        Save a string to a file
        :param filename:
        :param text: string
        :return: None
        '''
        if not isinstance(filename, (str, unicode)):
            raise TypeError
        if not isinstance(text, (str, unicode)):
            raise TypeError
        with open(filename, attr) as f:
            f.write(text)

    def RemoveBr(self, string):
        '''
        replace <BR> and \r with EOL
        remove &nbsp;
        :param string:
        :return: string
        '''
        ret = re.sub(u'<br/>', EOL, string)
        ret = re.sub(u'<br>', EOL, ret)
        ret = re.sub(u'\r', EOL, ret)
        ret = re.sub(u'[  \t　]+', u'', ret)
        ret = re.sub(u'\n{2,}', EOL, ret)
        return ret

    def GetNovelList(self):
        '''
        Get Novel List
        :param html_str: html string
        :return:
        '''
        html_str = self.novelListHtml

        soup = BeautifulSoup(html_str, 'lxml', from_encoding='utf-8')
        # print soup.title.string
        self.novel = self.GetNovelListDispatch(soup)
        self.fileName = self.novel['Title'] + u".txt"


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

    def GetNovelTextFromUrl(self, url):
        '''
        Get Novel Chapter Title and Text From Quyuege
        :param url: URL of WebSite
        :return: chapterText
        '''
        # open webpage and get html_str
        html_str = self.OpenWebPage(url)
        soup = BeautifulSoup(html_str, 'lxml', from_encoding='utf-8')

        title, text = self.GetNovelTextDispatch(soup)
        title = self.RemoveBr(title)
        text = self.RemoveBr(text)
        chapterText = title + EOL + text + EOL
        return chapterText

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

    def GetNovel(self, startChap = 0):
        '''
        DownLoad Text Start
        :return:
        '''
        self.GetNovelList()
        print self.novel['Title']
        # get novel
        novelTxt = self.novel['Title'] + EOL
        novelTxt += self.novel['Author'] + EOL
        novelTxt += self.novel['Abstract'] + EOL
        novelTxt = self.RemoveBr(novelTxt)
        novelTxt = novelTxt.encode('utf-8')
        novelTxt += self.webPageUrl + EOL.encode('utf-8') + EOL.encode('utf-8')

        self.SaveToFile(self.fileName, novelTxt)

        numIdx = startChap
        numChapter = len(self.novel['UrlList'])
        for novelUrl in self.novel['UrlList'][startChap:]:
            numIdx += 1
            print "[%4.3f%%] %5d of %5d is done ..." % (100.0 * numIdx / numChapter, numIdx, numChapter)
            textUrl = self.NovelUrlComb(novelUrl)
            chapterText = self.GetNovelTextFromUrl(textUrl).encode('utf-8')
            self.SaveToFile(self.fileName, chapterText, attr='a+')

        print '[Process Done]'

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    if len(sys.argv) < 2:
        print 'For debug usage!'
        webPageUrl = URL
    elif len(sys.argv) == 2:
        webPageUrl = str(sys.argv[1])
    elif len(sys.argv) == 3:
        webPageUrl = str(sys.argv[1])
        startChap = int(sys.argv[2]) - 1
    else:
        raise Exception("too many input parameters (>2)")

    novelDL = NovelDownloader(webPageUrl)
    novelDL.GetNovel(startChap)

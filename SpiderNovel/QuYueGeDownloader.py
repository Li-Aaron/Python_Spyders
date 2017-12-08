# -*- coding: utf-8 -*-
'''
程序名称 QuYueGeDownloader
@Author: AC
2017-12-8
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import urllib2,urllib
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
def OpenWebPage(url):
    '''
    Open a Webpage and return the html string
    :param url: URL of WebSite
    :return: HTML PAGES
    '''
    if not isinstance(url,(str)):
        raise TypeError
    user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(req)
    html = response.read()
    return html

def SaveToFile(filename, text, attr = 'w'):
    '''
    Save a string to a file
    :param filename:
    :param text: string
    :return: None
    '''
    if not isinstance(filename,(str,unicode)):
        raise TypeError
    if not isinstance(text,(str,unicode)):
        raise TypeError
    with open(filename, attr) as f:
        f.write(text)

def RemoveBr(string):
    '''
    replace <BR> and \r with EOL
    :param string:
    :return: string
    '''
    ret = re.sub(u'[<br/><br>]+', EOL, string)
    ret = re.sub(u'\r', EOL, ret)
    return ret

def GetNovelList(html_str):
    '''
    Get Novel List From Quyuege
    :param html_str: html string
    :return: novel : key('Title','Author','Abstract','UrlList')
    '''
    novel = {}
    soup = BeautifulSoup(html_str, 'lxml', from_encoding='utf-8')
    # print soup.title.string

    # novel title and properties
    novelProperties = soup.find_all('div', class_ = "rtext")[0]
    novel['Title'] = novelProperties.find_all('h1')[0].string
    novel['Author'] = novelProperties.find_all('a')[0].string
    novel['Abstract'] = novelProperties.find_all('div', class_ = "desc")[0].string

    # novel url list
    novelList = soup.find_all('div', "mod mod-article-list")[0]
    novelUrlList = []
    for novelUrl in novelList.find_all('a'):
        novelUrlList.append(novelUrl['href'])
    novel['UrlList'] = novelUrlList
    return novel

def GetNovelFromUrl(url):
    '''
    Get Novel Chapter Title and Text From Quyuege
    :param url: URL of WebSite
    :return: chapterText
    '''
    # open webpage and get html_str
    html_str = OpenWebPage(url)
    # SaveToFile('debug.html',html_str)
    soup = BeautifulSoup(html_str, 'lxml', from_encoding='utf-8')

    # find novel title
    title = soup.find_all('h1')[0].string
    title = RemoveBr(title)

    # find novel text
    novelText = soup.find_all('div', class_="page-content")[0]
    matchObj = re.search(u'固定结束-->(.*)</div>',unicode(novelText),re.M|re.S)
    if not matchObj:
        text = ''
    else:
        text = matchObj.group(1)
        # remove <br/>
        text = RemoveBr(text)

    chapterText = title + EOL + text + EOL
    return chapterText

##############################################
#------------------类定义--------------------#
##############################################


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
    else:
        raise Exception("too many input parameters (>2)")


    html = OpenWebPage(webPageUrl)
    novel = GetNovelList(html)

    print novel['Title']
    # get novel
    novelTxt = novel['Title'] + EOL
    novelTxt += novel['Author'] + EOL
    novelTxt += novel['Abstract'] + EOL
    novelTxt = RemoveBr(novelTxt)
    novelTxt = novelTxt.encode('utf-8')
    novelTxt += webPageUrl + EOL.encode('utf-8') + EOL.encode('utf-8')

    fileName = novel['Title']+u".txt"
    SaveToFile(fileName, novelTxt)

    numIdx = 0
    numChapter = len(novel['UrlList'])
    for novelUrl in novel['UrlList']:
        numIdx += 1
        print "[%4.3f%%] %5d of %5d is done ..." % (100.0*numIdx/numChapter, numIdx, numChapter)
        chapterText = GetNovelFromUrl(webPageUrl + novelUrl).encode('utf-8')
        SaveToFile(fileName, chapterText, attr = 'a+')

    print '[Process Done]'
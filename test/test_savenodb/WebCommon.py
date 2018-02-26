# -*- coding: utf-8 -*-
'''
程序名称 WebCommon
@Author: AC
2018-2-25
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import urllib2
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import json
import csv
import sys

##############################################
#------------------常量定义------------------#
##############################################
URL = 'http://www.baidu.com/'
EOL = u'\n'

##############################################
#------------------函数定义------------------#
##############################################
def DumpJson(obj, filename = 'json_dump.json'):
    with open(filename,'wb') as f:
        json.dump(obj,f,indent=4)

def LoadJson(filename = 'json_dump.json'):
    with open(filename, 'rb') as f:
        json_str = json.load(f)
    return json_str

def DumpCsv(headers, rows, filename = 'csv_dump.csv',delimiter=' ', quotechar='|'):
    with open(filename,'wb') as f:
        f_csv = csv.DictWriter(f,headers,delimiter=delimiter, quotechar=quotechar)
        f_csv.writeheader()
        f_csv.writerows(rows)

def LoadCsv(filename='csv_dump.csv',delimiter=' ', quotechar='|'):
    with open(filename, 'rb') as f:
        f_csv = csv.DictReader(f,delimiter=delimiter, quotechar=quotechar)
        headers = f_csv.fieldnames
        rows = []
        for row in f_csv:
            rows.append(row)
    return headers, rows

def SaveToFile(fileName, text, attr='w'):
    '''
    Save a string to a file
    :param filename:
    :param text: string
    :return: None
    '''
    if not isinstance(text, (str, unicode)):
        raise TypeError
    with open(fileName, attr) as f:
        f.write(text)

##############################################
#------------------类定义--------------------#
##############################################
class WebCommon(object):

    user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"

    def __init__(self, url):
        if not isinstance(url, (str)):
            raise TypeError('url mast be string')
        self.webPageUrl = url

    def OpenWebPage(self):
        '''
        Open a Webpage and return the html string
        :param url: URL of WebSite
        :return: HTML PAGES
        '''
        req = urllib2.Request(self.webPageUrl)
        req.add_header('User-Agent', self.user_agent)
        html = ''
        timeoutCount = 5
        while not html:
            try:
                response = urllib2.urlopen(req, timeout=20)
                html = response.read()
            except urllib2.URLError:
                if not timeoutCount:
                    raise urllib2.URLError('Timeout Failure')
                print '[Error] Time out retry %s' % self.webPageUrl
                timeoutCount -= 1
        return html

    def OpenWebPageReq(self):
        headers = {'User-Agent':self.user_agent}
        html = ''
        timeoutCount = 5
        while not html:
            try:
                req = requests.get(self.webPageUrl, headers=headers, timeout=20)
                html = req.text
            except requests.Timeout:
                if not timeoutCount:
                    raise requests.Timeout
                print '[Error] Time out retry %s' % self.webPageUrl
                timeoutCount -= 1
        return html


##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    webPageUrl = URL

    wc = WebCommon(webPageUrl)
    html = wc.OpenWebPage()
    html2 = wc.OpenWebPageReq()
    soup = BeautifulSoup(html,'lxml',from_encoding='utf-8')


    print repr(soup.contents[2].contents[1].contents[1]) #child list
    print type(soup.children) #child listiterator
    print repr(soup.title.parent) #parent list
    print type(soup.contents[2].contents[1].parents) #parent generator
    print EOL,

    # find_all, find
    print len(soup.find_all('a'))

    a = soup.find_all(lambda tag:tag.has_attr('class') and tag.has_attr('id'))
    print repr(a[0])
    print repr(soup.find(lambda tag:tag.has_attr('class') and tag.has_attr('id')))

    a = soup.find_all('a',href=re.compile("baidu.com"))
    print len(a)
    for string in a[:5]:
        print repr(string)
    print EOL,

    # find_all text,limit
    for string in soup.find_all(text=re.compile("About")):
        print string

    print len(soup.find_all(text=re.compile("baidu.com")))
    print len(soup.find_all(text=re.compile("baidu.com"), limit=2))
    print EOL,

    # select (CSS)
    print 1,soup.select("title")
    print 2,soup.select("title head html") # 逐层查找
    print 3,soup.select("html head title")
    print 4,soup.select("html title")
    print 5,soup.select("html > head > title")
    print 6,soup.select("html > title")
    print 7,soup.select("div > #head") # id = head
    print 8,soup.select("#head > .head_wrapper") # id = head > class = head_wrapper
    # > child   ~ sib   + child after
    print 9,soup.select("#head ~ .c-tips-container") # id = head ~ class = c-tips-container
    print EOL,

    print 1,soup.select(".c-tips-container") # class
    print 2,soup.select("#c-tips-container") # id
    print 3,soup.select("[class~=c-tips-container]") # class
    print 4,soup.select("div#c-tips-container") # id
    print 5,soup.select("a#c-tips-container") # id
    print 6,soup.select("a[href]") # has_attr
    print EOL,

    # lxml -> XPath
    html_et = etree.HTML(html)
    html_result = etree.tostring(html_et)
    # print html_result
    urls = html_et.xpath(".//*[@id='setf']/@href")
    print urls
# -*- coding: utf-8 -*-
'''
程序名称 DataTestNoDb
@Author: AC
2018-2-25
'''
__author__ = 'AC'

##############################################
# ------------------import--------------------#
##############################################
import WebCommon
from bs4 import BeautifulSoup
from lxml import etree
import re

##############################################
# ------------------常量定义------------------#
##############################################
URL = 'http://seputu.com/'
EOL = u'\n'

##############################################
# ------------------函数定义------------------#
##############################################


##############################################
# ------------------类定义--------------------#
##############################################


##############################################
# ------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    wc = WebCommon.WebCommon(URL)
    html = wc.OpenWebPage()
    # print html

    # bs and json
    soup = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
    content = []
    for mulu in soup.find_all(class_='mulu'):
        h2 = mulu.find('h2')
        if h2:
            h2_title = h2.string # book title
            chaps = []
            for a in mulu.find(class_='box').find_all('a'):
                href = a.get('href') # chapter urls
                # href = a['href']
                # print a['href'],a.get('href')
                box_title = a.get('title')
                # print a['title'], a.get('title'), a.string
                chapter_title = a.string # chapter title
                chaps.append({'url':href,'title':chapter_title})
            content.append({'title':h2_title,'content':chaps})

    WebCommon.DumpJson(content)
    # print WebCommon.LoadJson()

    # csv
    headers = ['ID','name']
    rows = [{'ID':1001,'name':'Mary'},
            {'ID':1002,'name':'Amy'},
            {'ID':1003,'name':'Dick'},
            ]
    WebCommon.DumpCsv(headers,rows)
    headers, rows = WebCommon.LoadCsv()
    print headers
    print rows

    # etree(XPath) and csv
    headers = ['book_title','chap_title','url','date']
    rows = []
    html_et = etree.HTML(html)
    div_mulus = html_et.xpath('.//div[@class="mulu"]')
    pattern = re.compile(r'\s*\[(.*)\]\s+(.*)')
    for div_mulu in div_mulus:
        div_h2 = div_mulu.xpath('./div[@class="mulu-title"]/center/h2/text()')
        if div_h2:
            div_h2_title = div_h2[0].encode('utf-8')
            # print div_h2_title
            div_urls = div_mulu.xpath('./div[@class="box"]/ul/li/a')
            for div_url in div_urls:
                href = div_url.xpath('./@href')[0]
                chapter_title = div_url.xpath('./text()')[0].encode('utf-8')
                box_title = div_url.xpath('./@title')[0].encode('utf-8')
                matchObj = pattern.search(box_title)
                if matchObj:
                    date = matchObj.group(1)
                    title = matchObj.group(2)
                    row = dict(zip(headers,[div_h2_title, title, href, date]))
                    rows.append(row)
    WebCommon.DumpCsv(headers, rows)





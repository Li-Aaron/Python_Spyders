# -*- coding: utf-8 -*-
'''
程序名称 HtmlParser
解析网页
@Author: AC
2018-2-26
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
from bs4 import BeautifulSoup
import urlparse
import re

##############################################
#------------------常量定义------------------#
##############################################


##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################
class HtmlParser(object):

    def Parser(self, page_url, html_content):
        '''
        parser of webpage
        :param page_url:
        :param html_content:
        :return: urls and data
        '''
        if not isinstance(page_url, (str, unicode)):
            raise TypeError('input page_url must be string or unicode not %s', type(page_url))
        if not isinstance(html_content, (str, unicode)):
            raise TypeError('input html_content must be string or unicode not %s', type(html_content))
        html_content = html_content.encode('utf-8') if isinstance(html_content, unicode) else html_content
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        '''
        get new urls from page
        :param page_url:
        :param soup:
        :return:
        '''
        new_urls = set()
        links = soup.find_all('a',href=re.compile(r'/item/.*'))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url,new_url)
            new_urls.add(new_full_url)
        return new_urls


    def _get_new_data(self, page_url, soup):
        '''
        get avalible data from page
        :param page_url:
        :param soup:
        :return:
        '''
        data = {}
        data['url'] = page_url
        # print data['url'],
        try:
            title = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
            data['title'] = title.get_text()
        except:
            data['title'] = u''
        # print data['title'],
        try:
            summary = soup.find('div', class_='lemma-summary')
            data['summary'] = summary.get_text()
        except:
            data['summary'] = u''
        # print data['summary']
        return data


##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    pass


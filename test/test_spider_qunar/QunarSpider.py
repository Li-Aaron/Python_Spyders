#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
程序名称 QunarSpider 简单的动态网页爬取
数据存储器
@Author: AC
2018-3-20
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
from Common import logger
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, datetime
import csv
##############################################
#------------------常量定义------------------#
##############################################
url = 'https://hotel.qunar.com/'
##############################################
#------------------函数定义------------------#
##############################################

##############################################
#------------------类定义--------------------#
##############################################
class QunarSpider(object):

    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.set_page_load_timeout(50)
        self.driver.implicitly_wait(10) # 控制间隔时间，浏览器反应（隐式等待）
        self.csv_filename = 'Qunar_%s.csv' % time.strftime('%Y%m%d%H%M', time.localtime())
        self._webpage_init(url)

    def _webpage_init(self, url):
        self.driver.get(url)
        self.driver.maximize_window() # 最大化显示
        logger.info('page init complete')

    def __del__(self):
        self.driver.close()
        logger.info('driver closed')
        pass

    def _hotel_search(self, to_city, from_date, to_date):
        '''
        从主页面进入搜索页面
        :param to_city: 去往城市
        :param from_date: 入住日期
        :param to_date: 退房日期
        :return:
        '''
        # 网页元素提取
        ele_toCity = self.driver.find_element_by_name('toCity')
        ele_fromDate = self.driver.find_element_by_name('fromDate')
        ele_toDate = self.driver.find_element_by_name('toDate')
        ele_search = self.driver.find_element_by_class_name('search-btn')
        logger.info('element init complete')

        # 网页操作（搜索）
        ele_toCity.clear()
        ele_toCity.send_keys(to_city)
        ele_toCity.click()
        ele_fromDate.clear()
        ele_fromDate.send_keys(from_date)
        ele_toDate.clear()
        ele_toDate.send_keys(to_date)
        ele_search.click()
        logger.info('hotel search complete')

        # 网页下拉
        try:
            # 显式等待
            elem = WebDriverWait(self.driver, 10).until(
                EC.title_contains(unicode(to_city))
            )
        except Exception,e:
            logger.error('page loading failed')
            logger.error(e)
        time.sleep(5)
        self.page_num = 1
        logger.info('page loading complete, page_num: %s' % self.page_num)

    def _hotel_nextpage(self, to_city):
        '''点击下一页按键'''
        assert EC.title_contains(unicode(to_city))(self.driver)
        assert EC.visibility_of(self.driver.find_element_by_css_selector('.item.next'))(self.driver)
        ele_nextpage = self.driver.find_element_by_css_selector('.item.next')
        ele_nextpage.click()
        time.sleep(5)
        self.page_num += 1
        logger.info('page loading complete, page_num: %s' % self.page_num)

    def _page_scroll(self):
        '''使用js脚本滚动页面到底端'''
        js = "window.scrollTo(0, document.body.scrollHeight);"
        self.driver.execute_script(js)
        time.sleep(5)
        logger.info('page scroll and loading complete, page_num: %s' % self.page_num)

    def _get_html_content(self):
        return self.driver.page_source

    def _html_content_parse(self, html_content):
        '''
        解析html
        :param html_content: unicode html content
        :return:
        '''
        def text_or_none(findobj):
            return findobj.text if findobj else 'none'

        hotel_dicts = []
        soup = BeautifulSoup(html_content, 'html.parser') # unicode content
        infos = soup.find_all(class_='item_hotel_info')
        for info in infos:
            hotel_dict = dict()
            hotel_dict['page_num'] = self.page_num
            hotel_dict['name'] = text_or_none(info.find(class_="e_title")).encode('utf-8')
            hotel_dict['rate'] = text_or_none(info.find(class_="score")).encode('utf-8')
            hotel_dict['area'] = text_or_none(info.find(class_="area_contair")).replace(' ','').replace('\t','').replace('\n','').encode('utf-8')
            hotel_dict['users'] = text_or_none(info.find(class_="js_list_usercomcount")).encode('utf-8')
            hotel_dict['price'] = text_or_none(info.find(class_="item_price")).encode('utf-8')
            hotel_dict['comment'] = text_or_none(info.find(class_="js_list_comment")).encode('utf-8')
            hotel_dicts.append(hotel_dict)
            logger.debug(hotel_dict)
        logger.info('hotel_dicts create complete, num = %s' % len(hotel_dicts))
        return hotel_dicts

    def _save_csv(self, headers, rows, filename='Crawled.csv', first_flag=True, *args, **kwargs):
        '''
        Save to Csv
        :param headers: row headers
        :param rows: datas
        :param filename:
        :param delimiter:
        :param quotechar:
        :param first_flag: if the file is first writen
        :return:
        '''
        if first_flag:
            with open(filename, 'wb') as fout:
                f_csv = csv.DictWriter(fout, headers, *args, **kwargs)
                f_csv.writeheader()
                f_csv.writerows(rows)
        else:
            with open(filename, 'ab') as fout:
                f_csv = csv.DictWriter(fout, headers, *args, **kwargs)
                f_csv.writerows(rows)

    def html_content_parse(self):
        '''
        获取网页+解析网页+存储csv封装
        '''
        html_content = self._get_html_content()
        hotel_dicts = self._html_content_parse(html_content)
        headers = hotel_dicts[0].keys()
        first_flag = False if self.page_num > 1 else True
        self._save_csv(headers,hotel_dicts,filename=self.csv_filename,delimiter=',',first_flag=first_flag)
        logger.info('csv saved complete, page_num = %s, first_flag = %s' % (self.page_num,first_flag))

    def crawl(self, to_city, from_date, to_date, page_max = 20):
        '''
        爬虫入口
        :param to_city: 去往城市
        :param from_date: 入住日期
        :param to_date: 退房日期
        :param page_max: 最大页面数
        :return:
        '''
        self._hotel_search(to_city, from_date, to_date)
        self._page_scroll()
        while self.page_num < page_max:
            self.html_content_parse()
            self._hotel_nextpage(to_city)
            self._page_scroll()

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    #
    page_max = 20
    to_city = u'上海'
    today = datetime.date.today()
    tomorrow = today+datetime.timedelta(days=1)
    from_date = today.strftime('%Y-%m-%d')
    to_date = tomorrow.strftime('%Y-%m-%d')

    spi = QunarSpider(url)
    spi.crawl(to_city, from_date, to_date, page_max)


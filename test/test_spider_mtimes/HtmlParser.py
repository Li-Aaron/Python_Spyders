# -*- coding: utf-8 -*-
'''
程序名称 HtmlParser (Mtimes)
解析网页
@Author: AC
2018-3-12
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
##############################################
from bs4 import BeautifulSoup
import urlparse
import re
import json
import traceback
from WebSpiCommon import logger

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

    def parser_json(self, page_url, response):
        '''
        parser of webpage(inside), 用于重构
        :param page_url:
        :param html_content:
        :return:
        '''
        pattern = re.compile(r'=(.*?);') #从 = 到 ;
        result = pattern.findall(response)[0]
        if result:
            value = json.loads(result) # json load
            try:
                isRelease = value.get('value').get('isRelease')
            except Exception,e:
                logger.error(repr(e))
                logger.error(traceback.format_exc())
                return None
            if isRelease: #是否上映
                if value.get('value').get('hotValue') == None: #是否热映
                    # 已经上映有票房显示
                    return self._parser_release(page_url, value)
                else:
                    # 正在热映没有票房显示
                    return self._parser_no_release(page_url, value)
            else:
                # 未上映没有票房显示
                return self._parser_no_release(page_url, value)

    def parser_urls(self, response):
        '''
        get new urls from response
        :param html_content:
        :return:
        '''
        # http://movie.mtime.com/218085/
        pattern = re.compile(r'(http://movie.mtime.com/(\d+)/)')
        new_urls = pattern.findall(response)
        if new_urls:
            return list(set(new_urls))
        else:
            return None

    def _parser_no_release(self, page_url, value):
        '''
        未上映的影片解析
        :param page_url: 电影链接
        :param value: json数据
        :return:
        '''
        try:
            isRelease = value.get('value').get('isRelease')
            movieRating = value.get('value').get('movieRating')
            movieTitle = value.get('value').get('movieTitle')


            # 评分信息
            RatingFinal = movieRating.get('RatingFinal')
            RPictureFinal = movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')
            RDirectorFinal = movieRating.get('RDirectorFinal')
            ROtherFinal = movieRating.get('ROtherFinal')

            # 电影信息
            MovieId = movieRating.get('MovieId')
            Usercount = movieRating.get('Usercount')
            AttitudeCount = movieRating.get('AttitudeCount')

            try:
                Rank = value.get('value').get('hotValue').get('Rank')
                Rank = 0 if Rank == None else Rank
            except:
                Rank = 0

            # 对应数据库15条信息
            data = (MovieId, movieTitle,
                    RatingFinal, RPictureFinal, RDirectorFinal, RStoryFinal, ROtherFinal,
                    Usercount, AttitudeCount,
                    u'None', u'None',
                    Rank, 0, isRelease)
            logger.debug('get data: %s' % (data,))
            return data
        except Exception, e:
            logger.error((repr(e), page_url, value))
            logger.error(traceback.format_exc())
            return None

    def _parser_release(self, page_url, value):
        '''
        已经上映的影片解析
        :param page_url: 电影链接
        :param value: json数据
        :return:
        '''
        try:
            isRelease = value.get('value').get('isRelease')
            movieRating = value.get('value').get('movieRating')
            boxOffice = value.get('value').get('boxOffice')
            movieTitle = value.get('value').get('movieTitle')

            # 评分信息
            RatingFinal = movieRating.get('RatingFinal')
            RPictureFinal = movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')
            RDirectorFinal = movieRating.get('RDirectorFinal')
            ROtherFinal = movieRating.get('ROtherFinal')

            # 电影信息
            MovieId = movieRating.get('MovieId')
            Usercount = movieRating.get('Usercount')
            AttitudeCount = movieRating.get('AttitudeCount')

            # 票房信息
            if boxOffice:
                TotalBoxOffice = boxOffice.get('TotalBoxOffice')
                TotalBoxOfficeUnit = boxOffice.get('TotalBoxOfficeUnit')
                TodayBoxOffice = boxOffice.get('TodayBoxOffice')
                TodayBoxOfficeUnit = boxOffice.get('TodayBoxOfficeUnit')
                ShowDays = boxOffice.get('ShowDays')
            else:
                TotalBoxOffice = '0'
                TotalBoxOfficeUnit = ''
                TodayBoxOffice = '0'
                TodayBoxOfficeUnit = ''
                ShowDays = 0

            try:
                Rank = boxOffice.get('Rank')
                Rank = 0 if Rank == None else Rank
            except Exception, e:
                Rank = 0
            # 对应数据库15条信息
            data = (MovieId, movieTitle,
                    RatingFinal, RPictureFinal, RDirectorFinal, RStoryFinal, ROtherFinal,
                    Usercount, AttitudeCount,
                    TotalBoxOffice + TotalBoxOfficeUnit, TodayBoxOffice + TodayBoxOfficeUnit,
                    Rank, ShowDays, isRelease)
            logger.debug('get data: %s' % (data,))
            return data
        except Exception, e:
            logger.error((repr(e), page_url, value))
            logger.error(traceback.format_exc())
            return None

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    pass


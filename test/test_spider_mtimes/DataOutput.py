# -*- coding: utf-8 -*-
'''
程序名称 DataOutput (Mtimes, Sqlite)
数据存储器
@Author: AC
2018-3-12
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import sqlite3
from WebSpiCommon import logger
'''
NULL	值是一个 NULL 值。
INTEGER	值是一个带符号的整数，根据值的大小存储在 1、2、3、4、6 或 8 字节中。
REAL	值是一个浮点值，存储为 8 字节的 IEEE 浮点数字。
TEXT	值是一个文本字符串，使用数据库编码（UTF-8、UTF-16BE 或 UTF-16LE）存储。
BLOB	值是一个 blob 数据，完全根据它的输入存储。
'''
##############################################
#------------------常量定义------------------#
##############################################

##############################################
#------------------函数定义------------------#
##############################################

##############################################
#------------------类定义--------------------#
##############################################
class DataOutput(object):

    table_name = 'MTimes'

    def __init__(self):
        self.con = sqlite3.connect("MTimes.db")
        self.cur = self.con.cursor()
        self.CreateTable(self.table_name)
        self.datas = []

    def __del__(self):
        if len(self.datas) > 0:
            self._output_db(self.table_name)
        self.con.close()

    def StoreData(self, data):
        if data is None:
            return
        self.datas.append(data)
        if len(self.datas) > 10:
            self._output_db(self.table_name)

    def CreateTable(self, table_name):
        '''
        创建表格
        :param table_name:
        :return:
        '''
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS %s(
                id INTEGER PRIMARY KEY,
                MovieId INTEGER,
                movieTitle VARCHAR(40) NOT NULL,
                RatingFinal REAL NOT NULL DEFAULT 0.0,
                RPictureFinal REAL NOT NULL DEFAULT 0.0,
                RDirectorFinal REAL NOT NULL DEFAULT 0.0,
                RStoryFinal REAL NOT NULL DEFAULT 0.0,
                ROtherFinal REAL NOT NULL DEFAULT 0.0,
                Usercount INTEGER NOT NULL DEFAULT 0,
                AttitudeCount INTEGER NOT NULL DEFAULT 0,
                TotalBoxOffice VARCHAR(20) NOT NULL,
                TodayBoxOffice VARCHAR(20) NOT NULL,
                Rank INTEGER NOT NULL DEFAULT 0,
                ShowDays INTEGER NOT NULL DEFAULT 0,
                isRelease INTEGER NOT NULL
            )
            '''%(table_name,))


    def _output_db(self, table_name):
        for data in self.datas:
            self.cur.execute('INSERT INTO %s (MovieId,movieTitle,'
                             'RatingFinal,RPictureFinal,RDirectorFinal,RStoryFinal,ROtherFinal,'
                             'Usercount,AttitudeCount,TotalBoxOffice,TodayBoxOffice,'
                             'Rank,ShowDays,isRelease) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'%(table_name,), data)
            logger.debug('save and removed data: %s'%(data,))
            self.datas.remove(data)
        self.con.commit()

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    pass


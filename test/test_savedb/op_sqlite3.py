#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
sqlite3 operators example
@Author: AC
2017-11-5
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
##############################################
import sqlite3

##############################################
#------------------常量定义------------------#
##############################################

##############################################
#------------------函数定义------------------#
##############################################

##############################################
#------------------类定义--------------------#
##############################################

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # 主线程
    # connection object
    con = sqlite3.connect(r'D:\Codes\Python\Python_Spyders\test\test_savedb\test.db') # 文件中创建
    # con = sqlite3.connect(':memory:') # 内存中创建

    # cursor object using to query
    cur = con.cursor()
    # select
    cur.execute('SELECT * FROM person LIMIT 100;')
    res = cur.fetchall()
    for line in res:
        print line

    cur.execute('SELECT * FROM person LIMIT 100;')
    res = cur.fetchone()
    print res
    res = cur.fetchone()
    print res

    # insert
    cur.execute('INSERT INTO person(name, age) VALUES ("Sapphire2",27);') # unsafe
    cur.execute('INSERT INTO person(name, age) VALUES (?,?)',('Sapphire3',28)) # safe
    cur.executemany('INSERT INTO person(name, age) VALUES (?,?)', [('Sapphire2', 28), ('Sapphire3', 29)])  # safe

    # delete
    cur.execute('DELETE FROM person WHERE id > ?;',(2,))

    # commit/rollback --> commit之前都不会真正写入，只是写到内存里，可以rollback掉
    con.commit()
    con.rollback() # can only rollback which was never committed

    # update
    cur.execute('UPDATE person SET age=? WHERE name=?',(28,'Sapphire'))
    cur.execute('SELECT * FROM person LIMIT 100;')
    res = cur.fetchall()
    for line in res:
        print line

    con.rollback()
    cur.execute('SELECT * FROM person LIMIT 100;')
    res = cur.fetchall()
    for line in res:
        print line
    con.close()
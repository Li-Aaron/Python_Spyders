#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
mysql operators example
@Author: AC
2017-11-5
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
##############################################
import MySQLdb

##############################################
#------------------常量定义------------------#
##############################################

##############################################
#------------------函数定义------------------#
##############################################
def load_mysql_info(filename):
    with open(filename) as f:
        host     = f.readline().replace('\n', '')
        port     = int(f.readline().replace('\n', ''))
        username = f.readline().replace('\n', '')
        password = f.readline().replace('\n', '')
    return host, port, username, password

##############################################
#------------------类定义--------------------#
##############################################

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # 主线程
    # connection object
    host, port, user, passwd = load_mysql_info('setting.txt')
    con = MySQLdb.connect(host=host,port=port,user=user,passwd=passwd,db='test',charset='gbk') # 文件中创建
    # con = sqlite3.connect(':memory:') # 内存中创建

    # cursor object using to query
    cur = con.cursor()
    # create database
    cur.execute('''CREATE TABLE student
(
    id INT unsigned not null auto_increment primary key,
    name VARCHAR(20) not null,
    sex VARCHAR(4) not null,
    age TINYINT unsigned not null
);
''')

    # insert
    cur.execute('INSERT INTO student(name, age, sex) VALUES ("Ruby",27,"M");') # unsafe
    cur.execute('INSERT INTO student(name, age, sex) VALUES (%s,%s,%s)'%("'Sapphire'","28","'F'")) # safe
    cur.execute('INSERT INTO student(name, age, sex) VALUES (%s,%s,%s)',('Sapphire',28,'F')) # safe
    cur.executemany('INSERT INTO student(name, age, sex) VALUES (%s,%s,%s)', [('Sapphire2', 28,'F'), ('Sapphire3', 29,'F')])  # safe

    # select
    cur.execute('SELECT * FROM student LIMIT 100;')
    res = cur.fetchall()
    for line in res:
        print line

    cur.execute('SELECT * FROM student LIMIT 100;')
    res = cur.fetchone()
    print res
    res = cur.fetchone()
    print res


    # delete
    cur.execute('DELETE FROM student WHERE id > %s;',(2,))

    # commit/rollback --> commit之前都不会真正写入，只是写到内存里，可以rollback掉
    con.commit()
    con.rollback() # can only rollback which was never committed

    # update
    cur.execute('UPDATE student SET age=%s WHERE name=%s',(28,'Sapphire'))
    cur.execute('SELECT * FROM student LIMIT 100;')
    res = cur.fetchall()
    for line in res:
        print line

    con.rollback()
    cur.execute('SELECT * FROM student LIMIT 100;')
    res = cur.fetchall()
    for line in res:
        print line

    cur.execute('DROP TABLE student;')
    con.commit()
    con.close()
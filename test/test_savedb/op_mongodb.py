#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
mongodb operators example
@Author: AC
2017-11-5
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
##############################################
import pymongo
import datetime


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
    # connect
    client = pymongo.MongoClient()
    # client = pymongo.MongoClient('localhost',27017)
    # client = pymongo.MongoClient('mongodb://localhost:27017')

    # get database
    db = client.TEST
    # db = client['TEST']

    # get collection(table)
    collection = db.books
    # collection = db['books']

    # insert document(row)
    book = {"author":"Dick",
            "text":"My First Book",
            "tags":["爬虫","Python","MongoDB"],
            "date":datetime.datetime.utcnow()
            }
    collection.insert_one(book)

    # select
    collection.find_one()
    collection.find_one({"author":"Dick"})

    book = {"author":"Ruby",
            "text":"My Second Book",
            "tags":["数据库","MongoDB"],
            "date":datetime.datetime.utcnow()
            }
    collection.insert_one(book)

    for book in collection.find():
        print book

    collection.find().count()

    # update
    collection.update_one({'author':'Ruby'},
                          {'$set':{'text':'Your Second Book'}})
    # collection.update_many({'author':'Ruby'},
    #                       {'$set':{'text':'Your Second Book'}})
    for book in collection.find():
        print book

    # remove
    collection.delete_one({'author':'Ruby'})
    # collection.delete_many({'author':'Ruby'})
    for book in collection.find():
        print book

    # close
    client.close()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
make weibo relation csv
@Author: AC
2018-4-27
'''

__author__ = 'AC'

import pymongo
import csv
import codecs

CODING = 'gbk'
DEGREE = 1

def save_csv(headers, rows, filename, delimiter=',', quotechar='|'):
    with open(filename,'wb') as f:
        f_csv = csv.DictWriter(f,headers,delimiter=delimiter, quotechar=quotechar)
        f_csv.writeheader()
        f_csv.writerows(rows)


if __name__ == '__main__':
    client = pymongo.MongoClient()
    db = client.weibo2
    info_collection = db.UserInfo
    relation_collection = db.Relation

    to_code = lambda x: x.encode(CODING) if isinstance(x,unicode) else x

    # 提取info
    results = info_collection.find()
    info_keys = ['user_id','username','degree']
    info_results = [{key: to_code(value) for key, value in result.items() if key in info_keys} for result in results]
    id_list = set(result['user_id'] for result in info_results if result['degree'] <= DEGREE)

    # 提取relation, 去掉id_list以外的关系
    relation_keys = ['user_id', 'relation_id']
    results = relation_collection.find({'relation_type':'follower'}) #只看关注者
    relation_results = [{key: to_code(value) for key, value in result.items() if key in relation_keys}
                        for result in results
                        if result['user_id'] in id_list and result['relation_id'] in id_list]

    # followee 转换成 follower 加到follower里
    results = relation_collection.find({'relation_type': 'followee'})  # 只看被关注者
    relation_results_2 = [{key: to_code(value) for key, value in result.items() if key in relation_keys}
                        for result in results
                        if result['user_id'] in id_list and result['relation_id'] in id_list]
    relation_results_2 = [{'relation_id':result['user_id'], 'user_id':result['relation_id']} for result in relation_results_2]
    relation_results.extend(relation_results_2)

    # 更新id_list, 更新info (去掉无关系人)
    user_id_list = set(result['user_id'] for result in relation_results)
    relation_id_list = set(result['relation_id'] for result in relation_results)
    new_id_list = user_id_list|relation_id_list
    new_info_results = [result for result in info_results if result['user_id'] in new_id_list]

    save_csv(info_keys, new_info_results, filename='UserInfo.csv')
    save_csv(relation_keys, relation_results, filename='Relation.csv')

    client.close()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import codecs
import Levenshtein
import logging
import random
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import scipy.io as scio
import sklearn
import matplotlib

logging.basicConfig(level=logging.INFO)

user_file = open('groundtruth.txt')
user_gp = user_file.readlines()
user_file.close()
same_line_dict = {}
for items in user_gp:
    users = items.strip().split()
    same_line_dict.update({x: users for x in users})
# print(same_line_dict)

info_file = codecs.open('new_posts.txt', 'r', 'utf-8')
info_data = info_file.readlines()
info_file.close()
info_dict = {}
for line in info_data:
    tmp_str = line.strip()
    # print(tmp_str)
    try:
        tmp_dict = json.loads(tmp_str)
        k = list(tmp_dict.keys())
        # print(k)
        v = tmp_dict[k[0]]
        info_dict.update({k[0]: v})
    except:
        logging.warning('Invalid Data!')
        continue

valid_users = list(info_dict.keys())
user_num = len(valid_users)
print(user_num)


def gen_label(uid1, uid2):
    if same_line_dict[uid1].__contains__(uid2) and same_line_dict[uid2].__contains__(uid1):
        return '1'
    else:
        return '-1'


info_keys = ['text', 'textLength', 'source', 'id', 'screen_name',
             'statuses_count', 'verified', 'verified_type',
             'description', 'gender', 'urank', 'followers_count',
             'follow_count', 'reposts_count', 'comments_count',
             'attitudes_count', 'isLongText']


def get_info(uid):
    if info_dict[uid] == []:
        return False, {}
    tdict = {
        'text': '',
        'textLength': 0,
        'source': '',
        'id': '',
        'screen_name': '',
        'statuses_count': 0,
        'verified': False,
        'verified_type': -1,
        'description': '',
        'gender': '',
        'urank': 0,
        'followers_count': 0,
        'follow_count': 0,
        'reposts_count': 0,
        'comments_count': 0,
        'attitudes_count': 0,
        'isLongText': False
    }
    # print(info_dict[uid])
    latest_po = info_dict[uid][0]['mblog']
    user_info = latest_po['user']
    # print(latest_po)
    # print(user_info)
    for elem in info_keys[0:3]:
        if list(latest_po.keys()).__contains__(elem):
            tdict.update({elem: latest_po[elem]})
    for elem in info_keys[3:]:
        if list(user_info.keys()).__contains__(elem):
            tdict.update({elem: user_info[elem]})
    return True, tdict


def gen_data(dict1, dict2):
    result = []
    if dict1['verified'] and dict2['verified']:
        verified = -1
    elif dict1['verified'] or dict2['verified']:
        verified = 1
    else:
        verified = 0
    result.append(verified)
    bool_style = ['verified_type', 'gender', 'isLongText']
    for items in bool_style:
        result.append(1 if dict1[items] == dict2[items] else 0)
    result.append(abs(dict1['urank'] - dict2['urank']))
    result.append(abs(dict1['statuses_count'] - dict2['statuses_count']))
    result.append(abs(dict1['followers_count'] - dict2['followers_count'])
                  / abs(dict1['followers_count'] + dict2['followers_count'])
                  if abs(dict1['followers_count'] + dict2['followers_count']) != 0
                  else 1)
    result.append(abs(dict1['follow_count'] - dict2['follow_count'])
                  / abs(dict1['follow_count'] + dict2['follow_count'])
                  if abs(dict1['follow_count'] + dict2['follow_count']) != 0
                  else 1
                  )
    result.append(abs(dict1['reposts_count'] - dict2['reposts_count']))
    result.append(abs(dict1['comments_count'] - dict2['comments_count']))
    result.append(abs(dict1['attitudes_count'] - dict2['attitudes_count']))
    result.append(Levenshtein.jaro_winkler(dict1['screen_name'], dict2['screen_name']))
    result.append(Levenshtein.jaro_winkler(dict1['description'], dict2['description']))
    result.append(Levenshtein.jaro_winkler(dict1['text'], dict2['text']))
    return result


logging.info('Prepare Data!')
train_num = 10000
data = []
labels = []
uidpool=[]
for i in range(0, train_num):
    order1 = random.randint(0, user_num - 1)
    order2 = random.randint(0, user_num - 1)
    uid1 = valid_users[order1]
    uid2 = valid_users[order2]
    if random.random() >= 0.001:
        # print('+-1')
        uid2 = same_line_dict[uid1][random.randint(0, len(same_line_dict[uid1]) - 1)]
    flag1, dict1 = get_info(uid1)
    flag2, dict2 = get_info(uid2)
    while (uid1 == uid2 or uidpool.__contains__([uid1,uid2]) or not flag1 or not flag2):
        order1 = random.randint(0, user_num - 1)
        order2 = random.randint(0, user_num - 1)
        uid1 = valid_users[order1]
        uid2 = valid_users[order2]
        flag1, dict1 = get_info(uid1)
        flag2, dict2 = get_info(uid2)
    uidpool.append([uid1,uid2])
    uidpool.append([uid2,uid1])
    data.append(gen_data(dict1, dict2))
    labels.append(gen_label(uid1, uid2))
    # print(uid1, uid2)
print(data)
print(labels)
print('total train number:', train_num)
print('pos_samples:', labels.count('1'))

logging.info('Start Training!')
rf = RandomForestClassifier(n_estimators=10, n_jobs=3,
                            verbose=0)
rf.fit(data[0:int(train_num/2)], labels[0:int(train_num/2)])

logging.info('Start Predict!')
print(rf.score(data[int(train_num/2):], labels[int(train_num/2):]))

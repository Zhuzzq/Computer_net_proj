#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import codecs
import Levenshtein
import logging
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import time
from sklearn.model_selection import KFold
import numpy as np
import scipy.io as scio
from matplotlib import pyplot as plt

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

flw_file = open('new_followings.txt')
flw_data = flw_file.readlines()
flw_file.close()
flw_dict = {}
for lines in flw_data:
    items = lines.strip().split()
    flw_dict[items[0]] = items[2:]
valid_flw = list(flw_dict.keys())
print(len(flw_dict))


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


def gen_flw(uid1, uid2):
    if not valid_flw.__contains__(uid1) and not valid_flw.__contains__(uid2):
        return 0, 0
    elif valid_flw.__contains__(uid1) and not valid_flw.__contains__(uid2):
        return flw_dict[uid1].__contains__(uid2), 0
    elif not valid_flw.__contains__(uid1) and valid_flw.__contains__(uid2):
        return flw_dict[uid2].__contains__(uid1), 0
    else:
        return 2, len(list(a for a in flw_dict[uid1] if a in flw_dict[uid2])) \
               / (
                   len(flw_dict[uid1]) + len(flw_dict[uid2]) - len(
                       list(a for a in flw_dict[uid1] if a in flw_dict[uid2])))


logging.info('Prepare Data!')
train_num = 8000
data = []
labels = []
uidpool = []
for i in range(0, train_num):
    order1 = random.randint(0, user_num - 1)
    order2 = random.randint(0, user_num - 1)
    uid1 = valid_users[order1]
    uid2 = same_line_dict[uid1][random.randint(0, len(same_line_dict[uid1]) - 1)]
    # uid2 = valid_users[order2]
    # if random.random() >= 0:
    #     # print('+-1')
    #     uid2 = same_line_dict[uid1][random.randint(0, len(same_line_dict[uid1]) - 1)]
    flag1, dict1 = get_info(uid1)
    flag2, dict2 = get_info(uid2)
    while (uid1 == uid2 or uidpool.__contains__([uid1, uid2]) or not flag1 or not flag2):
        order1 = random.randint(0, user_num - 1)
        order2 = random.randint(0, user_num - 1)
        uid1 = valid_users[order1]
        uid2 = valid_users[order2]
        flag1, dict1 = get_info(uid1)
        flag2, dict2 = get_info(uid2)
    uidpool.append([uid1, uid2])
    uidpool.append([uid2, uid1])
    tmp_data = gen_data(dict1, dict2)
    flw1, flw2 = gen_flw(uid1, uid2)
    # data.append(gen_data(dict1, dict2))
    tmp_data.append(flw1)
    tmp_data.append(flw2)
    data.append(tmp_data)
    labels.append(gen_label(uid1, uid2))
    # print(uid1, uid2)
print(data)
print(labels)
print('total number:', train_num)
print('total positive samples:', labels.count('1'))

logging.info('Start Training!')
rf = RandomForestClassifier(n_estimators=40, n_jobs=4, verbose=0)
accur = []
begin_time=time.time()
for order in range(0, 10):
    ratio = 9 / 10
    train_data = []
    train_labels = []
    test_data = []
    test_labels = []
    for i in range(0, train_num):
        if random.random() > ratio:
            test_data.append(data[i])
            test_labels.append(labels[i])
        else:
            train_data.append(data[i])
            train_labels.append(labels[i])

    # print('train number:', len(train_labels))
    # print('train positive samples:', train_labels.count('1'))
    rf.fit(train_data, train_labels)

    logging.info('Train Done!')

    # print('Train accuracy:',
    #       rf.score(train_data, train_labels))
    # print('Test accuracy:',
    #       rf.score(test_data, test_labels))
    acc = rf.score(data, labels)
    # print('Total accuracy:', acc)
    accur.append(acc)
end_time=time.time()
print('Feature Weight:')
# print('Feature Weight:', rf.feature_importances_)
features = ['verified', 'verified_type', 'gender', 'isLongText', 'urank', 'statuses_diff',
            'followers_diff', 'follows_diff', 'reposts_diff', 'comment_diff', 'attitudes_diff',
            'screen_name_similarity', 'description_similarity', 'text_similarity', 'co_follow', 'in_follows']
for i in range(0, 16):
    print(features[i], ':', rf.feature_importances_[i])

print('Total accuracy', rf.score(data, labels))

scores = cross_val_score(rf, data, labels, cv=10)
print(sum(scores) / 10)

print('time:',end_time-begin_time)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import codecs
import numpy as np
import scipy.io as scio
import sklearn
import matplotlib

user_file = open('groundtruth.txt')
user_gp = user_file.readlines()
user_file.close()
same_line_dict = {}
for items in user_gp:
    users = items.strip().split()
    same_line_dict.update({x: users for x in users})
print(same_line_dict)

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
        continue

valid_users = list(info_dict.keys())
print(len(valid_users))


def check_sameline(uid1, uid2):
    if same_line_dict[uid1].__contains__(uid2) or same_line_dict[uid2].__contains__(uid1):
        return 1
    else:
        return -1


info_keys = ['text', 'textLength', 'source', 'id', 'screen_name',
             'statuses_count', 'verified', 'verified_type',
             'description', 'gender', 'urank', 'followers_count',
             'follow_count', 'reposts_count', 'comments_count',
             'attitudes_count', 'isLongText']


def get_info(uid):
    if not valid_users.__contains__(uid):
        return 0, {}
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
    latest_po = info_dict[uid][0]['mlog']
    user_info = latest_po['user']
    tdict

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import codecs
import numpy as np
import scipy.io as scio
import sklearn
import matplotlib

file = codecs.open('new_info.txt', 'r', 'utf-8')
lines = file.readlines()
file.close()
dict = {}
linecnt = 1
for line in lines:
    tmp_str = line.strip()
    # print(linecnt)
    linecnt += 1
    tmp_dict = json.loads(tmp_str)
    dict[tmp_dict['id']] = tmp_dict
valid_user = dict.keys()
# print(valid_user)
# print(dict.keys())


# generate data

user_file = open('groundtruth.txt')
user_gp = user_file.readlines()
user_file.close()
labels = []
data = []

for items in user_gp:
    users=items.strip().split()
    users_info=[dict[each_user] for each_user in users
                if valid_user.__contains__(each_user)]
    if len(users_info)==1:
        tmpinfo=users_info[0]

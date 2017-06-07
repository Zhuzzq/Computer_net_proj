#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import codecs
import sklearn
import matplotlib

file = codecs.open('../info0.txt', 'r', 'utf-8')
lines = file.readlines()
file.close()
dict = {}
linecnt = 1
for line in lines:
    tmp_str = line.strip()
    print(linecnt)
    linecnt += 1
    tmp_dict = json.loads(tmp_str)
    dict[tmp_dict['id']] = tmp_dict
print(dict.keys())


def find_info(uid):
    tmpdict = dict[uid]

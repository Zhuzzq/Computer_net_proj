#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, json, codecs, random, time
import logging
from matplotlib import pyplot as plt

logging.basicConfig(level=logging.INFO)

# get the response
userfile = open('user.txt')
users = userfile.readlines()
userfile.close()
# cookiefile = open('cookie.txt')
# cookie = cookiefile.read().strip()

missing_user = []
wf = open('fans.txt', 'w')

for userid in users:
    userid = userid.strip()
    logging.info('user ID:' + userid)
    user_info = {}

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        'Connection': 'keep-alive',
        'Host': 'm.weibo.cn',
        'Referer': 'http://m.weibo.cn/p/second?containerid=100505%s_-_FANS' % userid,
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) '
                      'AppleWebKit/601.1.46 (KHTML, like Gecko) '
                      'Version/9.0 Mobile/13B143 Safari/601.1',
        'X-Requested-With': 'XMLHttpRequest'
    }

    URL = 'http://m.weibo.cn/api/container/getSecond?containerid = 100505%s_-_FANS' % userid

    try:
        h = requests.get(url=URL, headers=headers)
        if h.text:
            logging.info('First Connection Succeeded')
        else:
            logging.warning('First Connection Failed')

        # print(h.text)

        # get first page of followings and some info
        text = json.loads(h.text)
        # print(type(text))
        print(text)
        flwing_list = []
        if text['ok']:
            pagecnt = text['maxPage']
            # print(pagecnt)
            fllwingcnt = text['count']
            # print(pagecnt)
            # print(fllwingcnt)

            allusers = text['cards']
            # print(allusers)
            for dict_item in allusers:
                user_dict = dict_item['user']
                flwing_list.append(user_dict['id'])

            # get all followings
            for page in range(2, int(pagecnt) + 1):
                time.sleep(random.random() * 5)
                URL = 'http://m.weibo.cn/api/container/getSecond?containerid=100505%s_-_FANS&page=%d' % (
                    userid, page)
                h = requests.get(url=URL, headers=headers)
                text = json.loads(h.text)
                if text['ok'] == 1:
                    # print(text)
                    allusers = text['cards']
                    for dict_item in allusers:
                        user_dict = dict_item['user']
                        flwing_list.append(user_dict['id'])

                        # print(allusers)

        # user_info['flwing_cnt'] = len(allusers)
        wf.write(userid + ' ' + str(fllwingcnt))
        for nameid in flwing_list:
            wf.write(' ' + str(nameid))
        wf.write('\n')
        logging.info('Scratch Succeeded!')

    except:
        logging.warning('Scratch Failed!')
        missing_user.append(userid)
        time.sleep(random.random() * 11)

wf.close()
missing_file = open('fans_missing_list.txt', 'w')
for item in missing_user:
    missing_file.write(item + '\n')
missing_file.close()

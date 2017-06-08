#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, json, codecs, random, time
import logging
from matplotlib import pyplot as plt

logging.basicConfig(level=logging.INFO)

# get the response
userfile = open('new_posts_missing_list.txt')
users = userfile.readlines()
userfile.close()
# cookiefile = open('cookie.txt')
# cookie = cookiefile.read().strip()

wf = codecs.open('new_posts1.txt', 'w', 'utf-8')
missing_file = open('new_posts_missing_list1.txt', 'w')

for userid in users:
    userid = userid.strip()
    logging.info('user ID:' + userid)

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        'Connection': 'keep-alive',
        'Host': 'm.weibo.cn',
        'Referer': 'http://m.weibo.cn/u/%s?uid=%s&luicode=20000174&featurecode=20000180' % (userid, userid),
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) '
                      'AppleWebKit/601.1.46 (KHTML, like Gecko) '
                      'Version/9.0 Mobile/13B143 Safari/601.1',
        'X-Requested-With': 'XMLHttpRequest'
    }

    URL = 'http://m.weibo.cn/api/container/getIndex?uid=%s&luicode=20000174&' \
          'featurecode=20000180&type=uid&value=%s&' \
          'containerid=107603%s' % (userid, userid, userid)

    try:
        time.sleep(random.random() * 2 + 1)
        h = requests.get(url=URL, headers=headers)
        if h.text:
            logging.info('First Connection Succeeded')
        else:
            logging.warning('First Connection Failed')

        # get info
        text = json.loads(h.text)
        print(userid, text)
        latest_post = text['cards']
        wf.write('{' + userid + ':')
        json.dump(latest_post, wf, ensure_ascii=False)
        wf.write('}\n')
        logging.info('Scratch Succeeded!')


    except:
        logging.warning('Scratch Failed!')
        missing_file.write(userid + '\n')
        time.sleep(random.random() + 2)

wf.close()
missing_file.close()

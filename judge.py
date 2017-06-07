import requests
import json
import matplotlib

def info_scratch(uid):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        'Connection': 'keep-alive',
        'Host': 'm.weibo.cn',
        'Referer': 'https://m.weibo.cn/p/index?containerid=230283%s_-_'
                   'INFO&title=%25E5%259F%25BA%25E6%259C%25AC%25E4%25BF%25A1%25E6%2581%25AF&'
                   'luicode=10000011&lfid=230283%s&featurecode=20000180' % (uid, uid),
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) '
                      'AppleWebKit/601.1.46 (KHTML, like Gecko) '
                      'Version/9.0 Mobile/13B143 Safari/601.1',
        'X-Requested-With': 'XMLHttpRequest'
    }

def statistic_sockpuppet(uid1, uid2):
    info1=info_scratch(uid1)
    info2=info_scratch(uid2)



def judge_sockpuppet(uid1, uid2):
    result = False


    return result

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib
import requests
import time
import urllib
import hmac
from collections import OrderedDict

# coin
coin = 'eth'
public_key = 'u74wk-cdzj4-c1rgd-cezkr-8men3-had1b-suhwr'
private_key = '7jb6,-jz/${-htmf&-1zJy5-Q^s2&-R;[cU-Hj*Rq'
region = 'usc'
# type = 'buy'
# since = 'i.e'
id = '2709366'

# send requests
def request(method,params):
    Od = OrderedDict()
    Od['coin'] = coin
    Od['key'] = public_key
    Od['nonce'] = long(time.time())
    Od['region'] = region
    Od['id'] = id
    # Od['since'] = since
    # Od['type'] = type

    for i in params:
        Od[i] = params[i]

    Od['signature'] = signature(Od)
    response = requests.post('https://api.btctrade.im/api/v1/'+method,data=Od)
    # response = requests.get('https://api.btctrade.im/api/v1/'+method,data=Od)
    if response.status_code == 200:
        print(response.text)

# create signature
def signature(params):
    payload = urllib.urlencode(params)
    md5prikey = hashlib.md5(private_key).hexdigest()
    sign = urllib.quote(hmac.new(md5prikey, payload, digestmod=hashlib.sha256).hexdigest())
    return sign

# get balance
def balance():
    #查看订单信息
    request('trust_view',{})

    #挂单查询
     # request('trust_list',{})

    #账户信息
    # request('balance',{})

    #市场深度
    # request('depth',{})

balance()
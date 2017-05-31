# -*- coding: UTF-8 -*-
import hmac
import hashlib
import time


def login_signature(key, data):
    """
    为登录生成签名
    :param key: 签名密钥
    :param data: 带签名的数据
    :return:
    """
    msg = data['grant_type'] + data['client_id'] + data['source'] + str(int(time.time()))

    data['signature'] = hmac.new(
        bytes(key, 'utf-8'),
        bytes(msg, 'utf-8'),
        hashlib.sha1
    ).hexdigest()

# -*- coding: UTF-8 -*-
import json
import os
import sys
import time

import requests
import urllib3

from util.logger import logger
from config import CAPTCHA_URL, LOGIN_URL, CLIENT_SECRET, LOGIN_DATA, TOKEN_PATH
from .auth import BearerToken, OauthToken
from .exceptions import GetDataERRORException, NeedCaptchaException


class Client(object):
    def __init__(self):
        """
        客户端,所有操作的入口.
        """

        self._logger = logger

        self._token = None

        # 开启会话
        self._session = requests.session()

        # 设置 http 头信息
        self._session.headers.update({
            'User-Agent': 'com.zhihu.android/Futureve/5.1.1 Mozilla/5.0 (Linux; Android 4.4.4; 2014811 Build/KTU84P) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 '
                          'Google-HTTP-Java-Client/1.22.0 (gzip)',
            'x-api-version': '3.0.66',
            'x-app-version': '5.1.1',
            'x-app-za': 'OS=Android&Release=4.4.4&Model=2014811&VersionName=5.1.1&VersionCode=533&Width=720'
                        '&Height=1280&Installer=360&WebView=33.0.0.0DeviceType=AndroidPhoneBrand=Xiaomi',
            'x-app-build': 'release',
            'x-network-type': 'WiFi',
            'x-suger': 'SU1FST04Njc2MjIwMjQ1Njc4MDU7QU5EUk9JRF9JRD1jOTY1NGVkMzcwMWRjYjU1O01BQz05Yzo5OTphMDpiZjo3YzpjMQ',
            'x-udid': 'AGCCEL7IpwtLBdi3V7e7dsEXtuW9g1-pets=',
            'Connection': 'keep-alive',
        })

        # 不验证 ssl
        self._session.verify = False

        # 连接未验证的 HTTPS 请求时，不提示警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def login(self, username=None, password=None, load_token=True):
        """
        登录知乎
        默认会使用已保存的 token 进行登录
        :param username:
        :param password:
        :param load_token:
        :return:
        """

        # 自动加载已保存的 token
        if load_token:
            if self.load_token():
                return None

        # print('登录知乎,如果输入手机号,前缀请加"+86"')
        # 输入帐号密码
        username = username or input('email/phone: ')
        password = password or input('password: ')

        # 是否需要验证码
        try:
            if self.need_captcha():
                raise NeedCaptchaException
        except GetDataERRORException as e:
            log = '登录失败, {}'.format(str(e))
            self._logger.error(log)
            sys.exit(log)

        # 登录需要的参数
        data = LOGIN_DATA
        data['timestamp'] = int(time.time())
        data['username'] = username
        data['password'] = password

        # 添加签名 signature
        from .utils import login_signature
        login_signature(key=CLIENT_SECRET, data=data)

        # 发送登录请求
        response = self._session.post(LOGIN_URL, data=data, auth=OauthToken())
        token = response.json()

        # 登录失败,返回失败原因
        if 'error' in token:
            log = '登录失败, {}'.format(token['error']['message'])
            self._logger.error(log)
            sys.exit(log)
        else:
            self._token = token
            self._logger.info('登录成功，用户[%s]', username)
            # 登录成功 auth 更新
            self._session.auth = BearerToken(token['token_type'], token['access_token'])
            # 创建目录
            if not os.path.isdir(os.path.dirname(TOKEN_PATH)):
                os.makedirs(os.path.dirname(TOKEN_PATH))
            # 返回的数据保存到家目录中的 zhihu_token 文件中,以便下次使用
            with open(TOKEN_PATH, 'wb') as fp:
                fp.write(response.text.encode('utf-8'))

    def need_captcha(self):
        """
        是否需要验证码
        :return:
        """
        res = self._session.get(CAPTCHA_URL, auth=OauthToken())
        try:
            data = res.json()
            return data['show_captcha']
        except(KeyError, Exception):
            raise GetDataERRORException(CAPTCHA_URL, res)

    def show_captcha(self):
        pass

    def get_captcha(self):
        # print(self._session.get(CAPTCHA_URL).text)
        pass

    def load_token(self):
        """
        加载 token
        :return:
        """
        # 固定路径
        if os.path.isfile(TOKEN_PATH):
            with open(TOKEN_PATH, 'r') as fp:
                token = json.load(fp)
            self._token = token
            self._session.auth = BearerToken(token['token_type'], token['access_token'])
            self._logger.info('load token successful')
            return True
        return False

    def set_proxy(self, proxy_str=None):
        """
        设置代理
        :param proxy_str:
        :return:
        """
        if proxy_str is None:
            self._session.proxies.clear()
        else:
            self._session.proxies.update({'http': proxy_str, 'https': proxy_str})

    def myself(self):
        """
        我的信息
        :return:
        """
        from .models import Myself
        return Myself(self._token['uid'], self._session)

    def people(self, uid=None):
        """
        某个用户的相关信息及操作
        :param uid:
        :return:
        """
        from .models import People
        if uid is None:
            uid = self._token['uid']
        return People(uid, self._session)

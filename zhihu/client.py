# -*- coding: UTF-8 -*-
import requests
import requests.packages.urllib3 as urllib3
import time
import os
import sys
import json
from .configurations import CAPTCHA_URL, LOGIN_URL, CLIENT_SECRET, LOGIN_DATA, TOKEN_PATH, LOG_PATH
from .auth import BearerToken, OauthToken
from .exceptions import GetDataERRORException, NeedCaptchaException


class Client(object):
    def __init__(self):
        """
        客户端,所有操作的入口.
        """

        self._logger = None

        # 开启会话
        self._session = requests.session()

        # 不验证 ssl
        self._session.verify = False
        # 禁用 ssl 警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # 设置 http 头信息
        self._session.headers.update({
            'User-Agent': 'Futureve/4.50.0 Mozilla/5.0 (Linux; Android 4.4.4; 2014811 Build/KTU84P) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 '
                          'Google-HTTP-Java-Client/1.22.0 (gzip)',
            'x-api-version': '3.0.57',
            'x-app-version': '4.50.0',
            'x-app-za': 'OS=Android&Release=4.4.4&Model=2014811&VersionName=4.50.0&VersionCode=481&Width=720'
                        '&Height=1280&Installer=%E8%B1%8C%E8%B1%86%E8%8D%9A&WebView=33.0.0.0',
            'x-app-build': 'release',
            'x-udid': 'AGCCEL7IpwtLBdi3V7e7dsEXtuW9g1-pets=',
            'Connection': 'keep-alive',
        })

        self._token = None

    @property
    def logger(self, name='zhihu', filename=LOG_PATH):
        """
        日志
        :param name:
        :param filename:
        :return:
        """
        if self._logger:
            return self._logger

        import logging
        from logging.handlers import RotatingFileHandler

        # 创建保存目录
        if not os.path.isdir(os.path.dirname(LOG_PATH)):
            os.makedirs(os.path.dirname(LOG_PATH))
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = RotatingFileHandler(filename, mode='a', maxBytes=10 * 1024 * 1024, backupCount=6,
                                           encoding='utf-8')
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
        return self._logger

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

        print('登录知乎,如果输入手机号,前缀请加"+86"')
        # 输入帐号密码
        username = username or input('email/phone: ')
        password = password or input('password: ')

        # 是否需要验证码
        try:
            if self.need_captcha():
                raise NeedCaptchaException
        except GetDataERRORException as e:
            log = 'Login failed, reason: {}'.format(str(e))
            self.logger.error(log)
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
            log = 'Login failed, reason: {}'.format(token['error']['message'])
            self.logger.error(log)
            sys.exit(log)
        else:
            self._token = token
            self.logger.info('login successful username[%s]', username)
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
            self.logger.info('load token successful')
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
        return Myself(self._token['uid'], self._session, self.logger)

    def people(self, uid=None):
        """
        某个用户的相关信息及操作
        :param uid:
        :return:
        """
        from .models import People
        if uid is None:
            uid = self._token['uid']
        return People(uid, self._session, self.logger)

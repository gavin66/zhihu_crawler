# -*- coding: UTF-8 -*-


class ZhiHuException(Exception):
    pass


class GetDataERRORException(ZhiHuException):
    """
    获取数据时返回错误信息
    """

    def __init__(self, url, res):
        self._url = url
        self._res = res

        try:
            self._message = res.json()['error']['message']
        except (KeyError, Exception):
            self._message = None

    def __repr__(self):
        if self._message:
            return '获取数据时发生错误 --> {0}'.format(self._message)
        else:
            return '请求地址 [{self._url}] 发生未知错误 --> [{self.res.text}]'.format(self=self)

    __str__ = __repr__


class NeedCaptchaException(ZhiHuException):
    def __repr__(self):
        return 'Login requires Captcha'

# -*- coding: UTF-8 -*-

from .api_url import MYSELF_PROFILE_URL


class Myself(object):
    def __init__(self, session):
        self._url = MYSELF_PROFILE_URL
        self._session = session

    def info(self):
        """
        关于我的信息,json格式
        :return:
        """
        res = self._session.request('get', self._url)
        json_dict = res.json()
        return json_dict

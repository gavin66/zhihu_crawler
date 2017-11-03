# -*- coding: UTF-8 -*-
from config import MYSELF_PROFILE_URL, PEOPLE_FOLLOWEES_URL, PEOPLE_FOLLOWERS_URL
from .exceptions import GetDataERRORException
from util.logger import logger


class Base(object):
    def __init__(self, uid, session):
        self._uid = uid
        self._session = session
        self._logger = logger

    def _get_res(self, url, method='GET', params=None, data=None):
        res = self._session.request(
            method,
            url=url,
            params=params,
            data=data
        )
        return res

    def _get_data(self, url, method='GET', params=None, data=None):
        res = self._get_res(url, method, params, data)
        e = GetDataERRORException(url, res)
        try:
            data = res.json()
            if 'error' in data:
                raise e
            return data
        except Exception as e:
            raise e


class Myself(Base):
    def __init__(self, uid, session):
        super(Myself, self).__init__(uid, session)

    def info(self):
        """
        关于我的信息,json格式
        :return:
        """
        return self._get_data(MYSELF_PROFILE_URL)


class People(Base):
    def __init__(self, uid, session):
        super(People, self).__init__(uid, session)

    def followees(self, uid=None, limit=20, offset=0):
        """
        我关注的人
        :return:
        """
        return self._get_data(url=PEOPLE_FOLLOWEES_URL.format(uid if uid else self._uid),
                              params={'limit': limit, 'offset': offset})

    def followers(self, uid=None, url=None):
        """
        关注我的人
        :return:
        """
        if url:
            data = self._get_data(url)
        else:
            data = self._get_data(PEOPLE_FOLLOWERS_URL.format(uid if uid else self._uid),
                                  params={'limit': '20', 'offset': '0'})
        return data

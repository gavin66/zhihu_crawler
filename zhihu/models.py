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

    def followees(self, uid=None, page=1):
        """
        我关注的人
        如果 page 为 'all' 时，generator 参数被忽略，统一返回生成器
        :return:
        """
        if isinstance(page, int):
            offset = (page - 1) * 20
            res = self._get_data(url=PEOPLE_FOLLOWEES_URL.format(uid if uid else self._uid),
                                 params={'limit': 20, 'offset': offset})
            data = res['data']
            return data

    def generator_for_followees(self, uid=None, page=1):
        """
        我关注的人
        如果 page 为 'all' 时，generator 参数被忽略，统一返回生成器
        :return:
        """
        if isinstance(page, int):
            offset = (page - 1) * 20
            res = self._get_data(url=PEOPLE_FOLLOWEES_URL.format(uid if uid else self._uid),
                                 params={'limit': 20, 'offset': offset})
            data = res['data']
            for item in data:
                yield item
        elif isinstance(page, str) and page is 'all':
            res = self._get_data(url=PEOPLE_FOLLOWEES_URL.format(uid if uid else self._uid),
                                 params={'limit': 20, 'offset': 0})
            data = res['data']
            is_end = res['paging']['is_end']
            for item in data:
                yield item
            while not is_end:
                res = self._get_data(url=res['paging']['next'])
                data = res['data']
                is_end = res['paging']['is_end']
                for item in data:
                    yield item

    def followers(self, uid=None, limit=20, offset=0):
        """
        关注我的人
        :return:
        """
        return self._get_data(url=PEOPLE_FOLLOWERS_URL.format(uid if uid else self._uid),
                              params={'limit': limit, 'offset': offset})

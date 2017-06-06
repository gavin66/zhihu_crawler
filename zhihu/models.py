# -*- coding: UTF-8 -*-
import os
from .configurations import LOG_PATH
from .exceptions import GetDataERRORException
from .configurations import MYSELF_PROFILE_URL, PEOPLE_FOLLOWEES_URL, PEOPLE_FOLLOWERS_URL


class Base(object):
    def __init__(self, uid, session, logger=None):
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

    @property
    def logger(self, name='zhihu', filename=LOG_PATH):
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


class Myself(Base):
    def __init__(self, uid, session, logger=None):
        super(Myself, self).__init__(uid, session, logger)

    def info(self):
        """
        关于我的信息,json格式
        :return:
        """
        return self._get_data(MYSELF_PROFILE_URL)


class People(Base):
    def __init__(self, uid, session, logger=None):
        super(People, self).__init__(uid, session, logger)

    def followees(self, uid=None, url=None):
        """
        我关注的人
        :return:
        """
        if url:
            data = self._get_data(url)
        else:
            data = self._get_data(PEOPLE_FOLLOWEES_URL.format(uid if uid else self._uid),
                                  params={'limit': '20', 'offset': '0'})
        return data

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

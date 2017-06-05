# -*- coding: UTF-8 -*-
import os
from .setting import LOG_PATH
from .exception import GetDataERRORException


class Base(object):
    def __init__(self, uid, session, logger=None):
        self._uid = uid
        self._session = session
        self._logger = logger

    def _get_data(self, url, method='GET', params=None, data=None):
        res = self._session.request(
            method,
            url=url,
            params=params,
            data=data
        )

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

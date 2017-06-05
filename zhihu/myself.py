# -*- coding: UTF-8 -*-

from .api_url import MYSELF_PROFILE_URL
from .base import Base
from .exception import GetDataERRORException



class Myself(Base):
    def __init__(self, uid, session, logger=None):
        super(Myself, self).__init__(uid, session, logger)

    def info(self):
        """
        关于我的信息,json格式
        :return:
        """
        return self._get_data(MYSELF_PROFILE_URL)

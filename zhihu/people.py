# -*- coding: UTF-8 -*-

from .api_url import PEOPLE_FOLLOWEES_URL, PEOPLE_FOLLOWERS_URL

from .base import Base


class People(Base):
    def __init__(self, uid, session, logger=None):
        super(People, self).__init__(uid, session, logger)

    def followees(self):
        """
        我关注的人
        :return:
        """
        # res = self._session.request('get', PEOPLE_FOLLOWERS_URL.format(self._uid))
        # json_dict = res.json()
        # return json_dict
        data = self._get_data(PEOPLE_FOLLOWEES_URL.format(self._uid))
        return data

    def followers(self):
        """
        关注我的人
        :return:
        """
        data = self._get_data(PEOPLE_FOLLOWERS_URL.format(self._uid))
        return data

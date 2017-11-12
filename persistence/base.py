# -*- coding: UTF-8 -*-
class Base(object):
    def get_keep(self):
        raise NotImplementedError

    def get_next_keep(self):
        raise NotImplementedError

    def store_keep(self, user_id, zhihu_id):
        raise NotImplementedError

    def store_user(self, zhihu_id, data):
        raise NotImplementedError

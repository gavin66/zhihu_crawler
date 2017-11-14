# -*- coding: UTF-8 -*-
import sys
import os

sys.path.append(os.path.dirname(sys.path[0]))

from zhihu.client import Client
from persistence.mongodb_impl import MongoDB


class Profile(object):
    def __init__(self):
        self._zhihu_client = Client().login()
        # 登录后获取某个人信息
        self._people = self._zhihu_client.people()
        self._myself = self._zhihu_client.myself()
        self._persister = MongoDB()

    def run(self):
        user_id, zhihu_id = self._persister.get_keep()
        if user_id is None:
            myself_profile = self._myself.info()
            r = self._persister.store_user(myself_profile['id'], myself_profile)
            if r.upserted_id:
                user_id = r.upserted_id
                zhihu_id = myself_profile['id']
                self._persister.store_keep(r.upserted_id, myself_profile['id'])
        while user_id and zhihu_id:
            print('爬取用户 user_id = %s，zhihu_id = %s' % (user_id, zhihu_id))
            for user in self._people.generator_for_followees(zhihu_id, page='all'):
                self._persister.store_user(user['id'], user)
            try:
                # 执行下一个
                user_id, zhihu_id = self._persister.get_next_keep()
            except Exception as e:
                user_id = zhihu_id = False
                raise e
                # sys.exit('发生错误: ' + str(e))


if __name__ == '__main__':
    Profile().run()

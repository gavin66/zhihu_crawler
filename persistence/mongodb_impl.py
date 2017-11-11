# -*- coding: UTF-8 -*-
from persistence.base import Base
import pymongo
from config import MONGODB_URI


class MongoDB(Base):
    def __init__(self):
        self._client = pymongo.MongoClient(MONGODB_URI)
        self._db = self._client['zhihu']
        self._collection_user = self._db['user_profile']
        self._collection_keep = self._db['keep_on']

    def save(self):
        super().save()

    def get_keep(self):
        id_coll = self._collection_keep.find_one({'_id': 'zhihu_keep'}, {'user_id': 1, 'zhihu_id': 1})
        user_id = id_coll['user_id'] if id_coll else False
        zhihu_id = id_coll['zhihu_id'] if id_coll else False
        return user_id, zhihu_id

    
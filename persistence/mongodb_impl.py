# -*- coding: UTF-8 -*-
from persistence.base import Base
import pymongo
from config import MONGODB_URI
from bson.objectid import ObjectId


class MongoDB(Base):
    def __init__(self):
        self._client = pymongo.MongoClient(MONGODB_URI)
        self._db = self._client['zhihu']
        self._collection_user = self._db['user_profile']
        self._collection_keep = self._db['keep_on']
        self.zhihu_user_id = None
        self.zhihu_id = None

    def get_keep(self):
        if self.zhihu_user_id is None or self.zhihu_id is None:
            id_coll = self._collection_keep.find_one({'_id': 'zhihu_keep'}, {'user_id': 1, 'zhihu_id': 1})
            self.zhihu_user_id = id_coll['user_id'] if id_coll else None
            self.zhihu_id = id_coll['zhihu_id'] if id_coll else None
        return self.zhihu_user_id, self.zhihu_id

    def get_next_keep(self):
        try:
            # user_id = 5a07e14549d3d494065ac178，zhihu_id = 12545b636ef354d8d816c08862a3ec86
            # print('get_next_keep: zhihu_user_id %s zhihu_id %s' % (self.zhihu_user_id, self.zhihu_id))
            user = self._collection_user.find({'_id': {'$gt': ObjectId(self.zhihu_user_id)}}
                                              ).sort('_id', pymongo.ASCENDING).limit(1)[0]
            self.zhihu_user_id = user['_id']
            self.zhihu_id = user['id']
            self._collection_keep.update_one({'_id': 'zhihu_keep'},
                                             {'$set': {'user_id': self.zhihu_user_id, 'zhihu_id': self.zhihu_id}},
                                             upsert=True)
            return self.zhihu_user_id, self.zhihu_id
        except Exception as e:
            raise e

    def store_keep(self, user_id, zhihu_id):
        self.zhihu_user_id = user_id
        self.zhihu_id = zhihu_id
        return self._collection_keep.update_one({'_id': 'zhihu_keep'},
                                                {'$set': {'user_id': user_id, 'zhihu_id': zhihu_id}}, upsert=True)

    def store_user(self, zhihu_id, data):
        return self._collection_user.update_one({'id': zhihu_id}, {'$setOnInsert': data}, upsert=True)

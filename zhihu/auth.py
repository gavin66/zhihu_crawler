# -*- coding: UTF-8 -*-
from requests.auth import AuthBase


class OauthToken(AuthBase):
    def __call__(self, r):
        r.headers['Authorization'] = 'oauth 8d5227e0aaaa4797a763ac64e0c3b8'
        return r


class BearerToken(AuthBase):
    def __init__(self, auth_type, token):
        self._type = auth_type
        self._token = token

    def __call__(self, r):
        r.headers['Authorization'] = '{auth_type} {token}'.format(auth_type=str(self._type), token=str(self._token))
        return r

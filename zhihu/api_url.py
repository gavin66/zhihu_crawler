# -*- coding: UTF-8 -*-
API_URL = 'https://api.zhihu.com'

MYSELF_PROFILE_URL = API_URL + '/people/self'

# 用户相关操作 {} 填入用户 ID
PEOPLE_URL = API_URL + '/people/{}'

# 我关注的用户
PEOPLE_FOLLOWEES_URL = PEOPLE_URL + '/followees'

# 关注我的用户
PEOPLE_FOLLOWERS_URL = PEOPLE_URL + '/followers'



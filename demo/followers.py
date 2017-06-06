# -*- coding: UTF-8 -*-
from zhihu.client import Client
import json

# 所有程序的入口
client = Client()
# 直接使用用户名和密码登录
client.login(username='+8615555555555', password='password', load_token=True)
# 不使用参数,根据命令行输入
# client.login()

# 登录后获取某个人信息
people = client.people()

# 获取关注的人列表 前20条
# print(json.dumps(people.followees(), indent=4, ensure_ascii=False))

# 获取关注我的人(粉丝) 前20条
print(json.dumps(people.followers(), indent=4, ensure_ascii=False))


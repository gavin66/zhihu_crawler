# zhihu_crawler
自动登录,保存token,爬取知乎数据

# 使用方法

```python
from zhihu.client import Client

# 所有程序的入口
client = Client()
# 直接使用用户名和密码登录
client.login(username='+8615555555555', password='password')
# 不使用参数,根据命令行输入
# client.login()

# 登录后获取个人信息
myself = client.myself()

# 打印个人信息,json 格式
print(myself.info())
```


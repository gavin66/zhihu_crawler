# zhihu_crawler
[gavin66](https://github.com/gavin66)/[zhihu_crawler](https://github.com/gavin66) 使用知乎移动端 APP 的 API 爬取数据。



## 使用方法

> 你必须安装有 [mongoDB](https://www.mongodb.com/)

**安装依赖**

```sh
pip install -r requirements.tx
```

爬取用户信息保存进 mongodb 中

```sh
python zhihu_crawler/spider/profile.py
```



## 配置

文件 `config.py` 进行项目运行配置

```python
# mongodb 连接配置
MONGO_URI = 'mongodb://%s:%s@%s:%s/admin' % ('username', 'password', 'ip', 'port')

# 以下两个文件路径可随意换成你指定的
# token 默认保存地址
TOKEN_PATH = os.environ['HOME'] + '/zhihu_crawler/zhihu.token'
# 日志文件
LOG_PATH = os.environ['HOME'] + '/zhihu_crawler/zhihu.log'
```



## API 说明

```python
from zhihu.client import Client

# 所有程序的入口
client = Client()
# 直接使用用户名和密码登录
client.login(username='+8615555555555', password='password')
# 不使用参数,根据命令行输入
# client.login()

# 自己 model
myself = client.myself()
# 自己的信息
myself.info()

# 他人 model
people = client.people()
# 某人关注列表
people.followees()
# 某人被关注列表
people.followers()
```



## 运行截图

![](https://raw.githubusercontent.com/gavin66/zhihu_crawler/master/doc/p1.png)



## 参考

* 登录部分的实现在本人博客有说明 - [爬取知乎数据 - 模拟登录](http://blog.imgavin.me/2017/04/27/python-zhihu-api/)
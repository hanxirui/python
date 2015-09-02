#-*- coding:utf-8 -*-

'''
celery入门第一步，文件名称就是model名称
执行时需要先启动redis
执行(类似server)：
celery -A celerydemo worker --loglevel=info

调用：
from celerydemo import add,sayHello
add.delay(4, 4)
sayHello('world')

--------------------------------------------------------------------------------
----执行的日志输出
 -------------- celery@hanxiruideMacBook-Pro.local v3.1.18 (Cipater)
---- **** ----- 
--- * ***  * -- Darwin-14.5.0-x86_64-i386-64bit
-- * - **** --- 
- ** ---------- [config]
- ** ---------- .> app:         tasks111:0x103508c18
- ** ---------- .> transport:   redis://localhost:6379//
- ** ---------- .> results:     disabled
- *** --- * --- .> concurrency: 4 (prefork)
-- ******* ---- 
--- ***** ----- [queues]
 -------------- .> celery           exchange=celery(direct) key=celery
                

[tasks]
  . celerydemo.add
  . celerydemo.sayHello
----------------------------------------------------------------------------------

Celery 是一个广泛应用于网络应用程序的任务处理系统。

它可以在以下情况下使用:

在请求响应周期中做网络调用。服务器应当立即响应任何网络请求。如果在请求响应周期内需要进行网络调用，则应在周期外完成调用。例如当用户在网站上注册时，需要发送激活邮件。发送邮件是一种网络调用，耗时2到3秒。用户应该无需等待这2到3秒。因此，发送激活邮件应当在请求响应周期外完成，celery 就能实现这一点。

将一个由几个独立部分组成的大任务分成多个小任务。假设你想知道脸书用户的时间流。脸书提供不同的端点来获取不同的数据。譬如，一个端点用以获取用户时间流中的图片，一个端点获取用户时间流中的博文，一个端点得到用户的点赞信息等。如果你的函数需要和脸书的5个端点依此通信，每个网络调用平均耗时2秒，你将需要10秒完成一次函数执行。但是，你可以把这项工作分为5个独立的任务（你很快就会发现这很容易做到），并让 celery 来处理这些任务。Celery 可以并行地与这5个端点通信，在2秒之内就能得到所有端点的响应。
'''

from celery import Celery
from urllib import request

# ‘tasks’ 这个名称无所谓
app = Celery('celerydemo', broker='redis://localhost')

@app.task
def add(x, y):
    return x + y


@app.task
def sayHello(name):
    return 'Hello,' + name

@app.task
def fetch_url(url):
    with request.urlopen(url) as f:
        # data = f.read()
        print('Status:', f.status, f.reason)
 
def func(urls):
     for url in urls:
       fetch_url.delay(url)
    
if __name__ == "__main__":
     func(["http://oneapm.com", "http://jd.com", "https://taobao.com", "http://baidu.com"])













    
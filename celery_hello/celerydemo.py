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
'''

from celery import Celery

# ‘tasks’ 这个名称无所谓
app = Celery('tasks111', broker='redis://localhost')

@app.task
def add(x, y):
    return x + y


@app.task
def sayHello(name):
    return 'Hello,' + name
#-*- coding:utf-8 -*-

from celery import Celery

# ‘tasks’ 这个名称无所谓
app = Celery('tasks111', broker='redis://localhost')

@app.task
def add(x, y):
    return x + y


@app.task
def sayHello(name):
    return 'Hello,' + name
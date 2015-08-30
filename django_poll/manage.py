#!/usr/bin/env python3
#-*- coding:utf-8 -*-
'''
django提供的样例，一个投票程序。
使用python3和django1.8
是学习django的入门例子
'''
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_poll.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

#/usr/local/bin python3
#-*- coding:utf-8 -*-

'''一些python基础知识'''

adict = {'Michael': 95, 'Bob': 75, 'Tracy': 85}

alist = [
        '%s--- %s' % (key, value) for key, value in sorted(adict.items())
    ]
print(alist)

#/usr/local/env python3
#-*- coding:utf-8 -*-


def scope_test():
    def do_local():
        spam = "local spam"#局部变量
    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"#域变量，在整个函数域有效。
    def do_global():
        global spam
        spam = "global spam"#
    spam = "test spam"#全局变量，此处在函数域外有效；
    do_local()
    print("After local assignment:", spam)
    do_nonlocal()
    print("After nonlocal assignment:", spam)
    do_global()
    print("After global assignment:", spam)
scope_test()
print("In global scope:", spam)#全局变量作用域
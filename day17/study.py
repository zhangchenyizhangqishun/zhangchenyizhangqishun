#!/usr/env/bin python
# -*- coding:utf-8 -*-
# _author:zhangxiao
# Create Time = 2020/2/27

import sys
print sys.path


def bar():
    print "OK"
    count = yield 1
    print "count = %s"%count

    yield 2

b = bar()

print "b.send(None) = %s"%b.send(None)
b.send("111")
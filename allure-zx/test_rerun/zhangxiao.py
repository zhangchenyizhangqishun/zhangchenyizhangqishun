#!/usr/env/bin python
# -*- coding: utf-8 -*-
#__author:zhangxiao
#date: 2020-09-12


def test(aa):
    list_aa=list(aa)
    for i in range(len(list_aa)):
        value = list_aa[i]
        if 64< ord(value) <97:
            list_aa[i]=chr(ord(value)+32)
        # if value == chr(65):
        #     list_aa[i]="a"

    str_aa1=''.join(list_aa)
    return str_aa1



print test("AdfgA")

print "str_aa1:%s"%test("AdfgDHSJKICNDFBFJA")



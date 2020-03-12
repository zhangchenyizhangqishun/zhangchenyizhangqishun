#!/usr/env/bin python
# -*- coding:utf-8 -*-
# _author:zhangxiao
# Create Time = 2020/2/27

"""
使用装饰器知识，编写登录脚本
遇到book 使用账号密码登录
遇到shopping 使用微信登录

"""

flog_login = False

content = """ 
    *****************请选择*****************
    1:book
    2:shopping
    3:home

"""
def outer(author_type):
    def decortaor(func):
        def login():
            global flog_login
            if flog_login is False:
                if author_trance(author_type):
                    print "登录成功"
                    flog_login = True
                    func()
                else:
                    print "登录失败"
            else:
                func()
        return login
    return decortaor

@outer("jingdong")
def book():
    print "go book"

@outer("weixin")
def shopping():
    print "go shopping"

@outer("weixin")
def home():
    print "go home"

def author_trance(author_type):
    username = raw_input("请输入用户名：")
    password = raw_input("请输入密码： ")

    if author_type == "jingdong":
        print "----------------京东账户登录中--------------------"
        return action_login(username,password,author_type)
    elif author_type == "weixin":
        print "----------------微信账户登录中--------------------"
        return action_login(username, password, author_type)

def action_login(username,password,author_type):
    ret = get_data(author_type)
    # print "ret = %s" % ret.keys()
    # print "ret.keys() = %s" % type(str(ret.keys()))
    # print str(ret.keys())
    # print ret[username]
    # print ret
    if username !="q" or password !="q":
        if username in ret.keys():
            # print "ret[username] = %s"%ret[username]
            if ret[username] == password:
                # print "登录成功！！！"
                return True
            else:
                print "******用户名或密码错误，请重新输入!!!!******"
                author_trance(author_type)
        else:
            print "******用户名或密码错误，请重新输入******"
            author_trance(author_type)
    else:
        return False


def get_data(author_type):
    data = {}
    f = open(author_type,"r")
    for line in f.readlines():
        key ,value = line.strip().split(":")
        data[key]=value
    # print data
    # print data["zhangxiao"]
    f.close()
    return data

while True:
    print content
    chiose = int(raw_input(">>>"))
    # while True:
    if chiose == 1:
        book()
    elif chiose == 2:
        shopping()
    elif chiose == 3:
        home()
    else:
        print "输入错误"

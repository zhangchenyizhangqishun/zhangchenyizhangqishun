#!/usr/env/bin python
# -*- coding:utf-8 -*-
# _author:zhangxiao
# Create Time = 2020/3/5

import socket
import os
sk = socket.socket()

addrs = ("192.168.1.48",8000)
sk.bind(addrs)
sk.listen(6)
# conn,add = sk.accept()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

while 1:
    conn, add = sk.accept()
    while 1:
        # try:
        conn_data = conn.recv(1024)   # 接收
        cmd,file_name,file_size = conn_data.split("|")
        file = os.path.join(BASE_DIR, "copydir", file_name)
        f = open(file,"ab")
        # if method == "post":
        # print file
        # print cmd
        # print file_name
        print type(int(file_size))
        flog_size = 0
        file_size = int(file_size)
        while flog_size != file_size:

            f_write = conn.recv(1024)
            f.write(f_write)
            flog_size += len(f_write)
            # print "flog_size %s"%type(flog_size)
            # print "file_size %s"%file_size
        f.close()

        # except Exception as e:
        #     print e
        # if conn_data == "q":
        #     print "客户端已退出通讯！！！"
        #     break
        # print "conn_data = %s"%conn_data
        # inp = raw_input(">>>")
        # conn.send(inp)

    conn.close()
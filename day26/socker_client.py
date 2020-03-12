#!/usr/env/bin python
# -*- coding:utf-8 -*-
# _author:zhangxiao
# Create Time = 2020/3/5

import socket
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))



sk = socket.socket()

addrs = ("192.168.1.48",8000)
sk.connect(addrs)

while 1:
    inp_data = raw_input(">>>").strip()
    cmd,file_name = inp_data.split('|')
    file_path = os.path.join(BASE_DIR, file_name)
    file_name = os.path.basename(file_path)
    file_size = os.stat(file_name).st_size
    file_info = "%s|%s|%s"%(cmd,file_name,file_size)
    sk.sendall(file_info)
    # print "***************************"
    f = open(file_path, "rb")
    flog_size = 0
    while flog_size != file_size:
        # print "................................"
        f_read = f.read(1024)
        sk.sendall(f_read)
        flog_size += len(f_read)
    f.close()
    print "上传成功"
    # if inp_data == "q":
    #     break
    # client_recv_data = sk.recv(1024)
    # print "client_recv_data = %s"%client_recv_data

# sk.close()
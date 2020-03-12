#!/usr/env/bin python
# -*- coding:utf-8 -*-
# _author:zhangxiao
# Create Time = 2020/2/24

import json
# file_name = {"陕西省":{"西安市":{"莲湖区":"远东一中","高新区":"高新一中","雁塔区":"雁塔一中"},"咸阳市":{"秦都区":"咸阳一中"},"渭南市":{"临渭区":"渭南一中"}},"浙江省":{"杭州市":{"滨江区":"西兴中学"}},"上海市":{"徐汇区":"上海一中"}}


file_write = open("file_copy","w")
# file_write.write(file_name)
# file_write.close()
flog = True
new_lines = []
file_read = open("file","r")
lines =  file_read.readlines()
print "字符类型%s"%type(lines)
# line_dict = json.loads(lines,encoding='utf-8')



new_line_dice = {}

for line in lines:
    # file = eval(file)
    line_dict = json.loads(line)
    new_line_dice = line_dict
    # print file
print new_line_dice
while flog:
    for k in new_line_dice:
        print k
    input_data = str(raw_input("请输入信息："))
    input_data = input_data.decode('utf8')
    if input_data in new_line_dice:
        new_lines.append(new_line_dice)
        new_line_dice = new_line_dice[input_data]
    elif input_data =='b':
        if new_lines:
            new_line_dice = new_lines.pop()
    elif input_data =='q':
        flog = False
    elif input_data == 'w':
        new_write_data = raw_input("请输入添加信息：")
        file_write.write(new_write_data)
    else:
        print "请重新输入"

file_read.close()
file_write.close()
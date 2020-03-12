#!/usr/env/bin python
# -*- coding:utf-8 -*-
# _author:zhangxiao
# Create Time = 2020/2/24
import json

f = open("file_backup",'r')
# f_read = f.read()
dic_f = json.loads(f.read())
for i in dic_f:
    print i

f.close()


print

# line_dict = {"上海市": {"徐汇区": "上海一中"}, "陕西省": {"西安市": {"雁塔区": "雁塔一中", "高新区": "高新一中", "莲湖区": "远东一中"}, "渭南市": {"临渭区": "渭南一中"}, "咸阳市": {"秦都区": "咸阳一中"}}, "浙江省": {"杭州市": {"滨江区": "西兴中学"}}}
# flog = True
# new_lines = []
# while flog:
#     for k, v in line_dict.iteritems():
#         print 'key = %s' % k
#     input_data = raw_input("请输入信息：")
#     if input_data in line_dict:
#         new_lines.append(line_dict)
#         line_dict = line_dict[input_data]
#     elif input_data == 'b':
#         if new_lines:
#             line_dict = new_lines.pop()
#     elif input_data == 'q':
#         flog = False
#     else:
#         print "请重新输入"

# import codecs
# file_read = open("file","r")
# lines =  file_read.readlines()
# # print "字符类型%s"%type(lines)
# new_line_dice = {}
# for line in lines:
#     line_dict = json.loads(line)
#     new_line_dice = line_dict
# print new_line_dice
#
# flog = True
# new_lines = []
# while flog:
#     number = 0
#     # write_line = int(raw_input("请输入需要添加信息的行数："))
#     # f1_read = open("data1", "r")
#     f2_write = codecs.open("data2", "w",'utf-8')
#     for i in new_line_dice:
#         i = i.encode('utf-8')
#         print type(i)
#
#         f2_write.write(i)
#     isadd = raw_input("是否添加信息，y添加，其余不添加：")
#     if isadd !='y':
#         input_data = str(raw_input("请输入信息："))
#         input_data = input_data.decode('utf8')
#         if input_data in new_line_dice:
#             new_lines.append(new_line_dice)
#             new_line_dice = new_line_dice[input_data]
#         # elif input_data
#         # number +=1
#         # if number == 2 :
#         #     write_data = raw_input("请输入信息：")
#         #     i = i +write_data +"\n"
#         # f2_write.write(i)
#     else:
#         add_data = raw_input("请输入添加的信息：").decode('utf8')
#
#         f2_write.write(add_data)
#     # f1_read.close()
#     f2_write.close()
#
#     f2_read = open("data2", "r")
#     f1_write = open("data1", "w")
#     for i in f2_read.readlines():
#         f1_write.write(i)
#     f2_read.close()
#     f1_write.close()
#
# dicectory = {}
# new_dic = []
# with open('file','r') as f_read ,open("file_backup",'w') as f_write:
#     for line in f_read.readlines():
#         dicectory = line
#         print line
#     f_write.write(dicectory)
#     while True:
#         # for k in dicectory:
#         #     print k
#         input_data = str(raw_input("请输入信息："))
#         input_data = input_data.decode('utf-8')
#         if input_data in dicectory:
#             new_dic.append(dicectory)
#             dicectory = dicectory[input_data]


# def print_info(sex = 'man',*args,**kwargs):
#     print sex
#     print args
#
# dd = print_info
# print dd('asd',1,2,3,4)
# print type(eval('1+3*2'))
#
#
# map()
# #
# def f(n):
#     return n+ n
#
# def tt(a,b,f):
#     return f(a)+f(b)
#
# print tt(3,4,f)
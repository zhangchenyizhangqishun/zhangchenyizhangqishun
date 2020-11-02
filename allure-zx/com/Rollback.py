#!/usr/bin/env python
# _*_ coding:UTF-8

'''
Created on 2017-10-20

@author: hzhuangfg
@modify: hzhuangfg

回滚操作的包
'''

import time
import traceback
import sys

class ActionRollback:
    '''仿真事务的一个类
    当执行一些操作时，需要执行很多个步骤，当执行到一个中间的步骤失败时，需要倒序回滚前面的各个步骤
    '''

    def __init__(self):

        # 操作列表，每一步在列表中有一项，每一项是包括两个元索的数组，
        # 第一个元素是一个回滚函数，另一个元素是调用回滚函数的参数
        self.actions = []

    def rollback(self):
        '''回滚操作
        '''

        for action in self.actions[::-1]:
            action[0](*action[1])



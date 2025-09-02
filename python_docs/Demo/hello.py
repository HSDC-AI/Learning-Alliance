#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 模块注释文档 '

__author__ = '作者的名字'

import sys

def test():
    args = sys.argv
    if len(args) == 1:
        print('hello world')
    elif len(args) == 2:
        print(f'hello, {args[1]}!')
    else:
        print('too many arguments!')
        
def _private_test():
    print('this is a private test')

if __name__ == '__main__':
    test()
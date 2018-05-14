#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
__mktime__ = '2018/4/8 0008'
__author__ = 'Administrator'
__filename__ = 'charrdetTest'
"""

#coding=utf8
# from chardet import detect
# print(detect("你好".encode("utf-8")))
import sys,os

for  folder in os.walk(".").next()[1]:
    print(folder.decode(sys.stdin.encoding))
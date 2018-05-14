#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/23 0023'
__author__ = 'Administrator'
__filename__ = 'test'
"""
def uniform_symbology(tokes):
    new_tokes = [toke.replace(" ","").replace(", ","，").replace(".","。").replace(":","：") for toke in tokes]
    return new_tokes

if __name__ == '__main__':
    tokes = ["我","你好",",","好的",".",":","   "]
    new_tokes = uniform_symbology(tokes)
    print(new_tokes)
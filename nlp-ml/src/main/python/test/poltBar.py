#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/19 0019'
__author__ = 'Administrator'
__filename__ = 'poltBar'
"""

import json
import matplotlib.pyplot as plot
import numpy as np


def plotbarn(lists, x_name, title, rootPath, png_name):
    plot.figure(figsize=(10, 8))
    plot.hist(lists, bins=100, label=png_name)
    # if "match" in x_name:
    #     plot.legend(loc=0)
    # else:
    #     loc = int(np.mean(lists))
    #     plot.legend(loc=loc)
    plot.grid(True)
    plot.xlabel(x_name)
    plot.ylabel("count")
    plot.title(title)
    plot.savefig(fname=rootPath + png_name, format='png')


def readDict(path, file_name):
    f = open(path + file_name, "r")
    a = f.read()
    data = eval(a)
    f.close()
    return data


def data_deal(data, min_count, min_v):
    lists = []
    sumNum = 0
    for w, c in data:
        sumNum += c
        if min_count is not None and min_v is not None:
            if c > min_count and w > min_v:
                for i in range(0, c):
                    lists.append(w)
    return lists, sumNum


def scale(data, sumNum, is_inverted_order,thrsord):
    if is_inverted_order:
        num_95 = sumNum * (1 - thrsord)
    else:
        num_95 = sumNum * thrsord
    numS = 0;
    for w, c in data:
        numS += c
        if numS > num_95:
            print("95% 的阀值数据在 = " + str(w))
            break

def scaleRation(data, sumNum, num):

    numS = 0;
    for w, c in data:
        numS += c
        if w > num:
            ratio = round((float(numS)/float(sumNum))*100,2)
            print("95% 的阀值数据在 = " + str(ratio) + "%")
            break


if __name__ == '__main__':
    path = "E:/baiduCr/static/test/dict/"
    file_name = "test_question_seg_length_dict.txt"
    three_Q = 0.9973
    # x_name = "test_question_seg_length_cut"
    # png_name = "test_question_seg_length.png"
    # title = "test_question_seg_length_cut"
    tuple = readDict(path=path, file_name=file_name)
    lists, sumNum = data_deal(data=tuple, min_count=0, min_v=0)
    scale(tuple, sumNum, is_inverted_order=False,thrsord=0.95)
    # scaleRation(tuple,sumNum,50)
    # plotbarn(lists, x_name=x_name, title=title, rootPath=path, png_name=png_name)

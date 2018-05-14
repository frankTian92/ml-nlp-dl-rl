#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/24 0024'
__author__ = 'Administrator'
__filename__ = 'fastText_preprocess'
"""'''
合并json文件
'''
import json

def trans_lable(lable):
    if lable=="No":
        return str(0)
    if lable =="Depends":
        return str(1)
    if lable=="Yes":
        return str(2)


def combine():
    rootPath = "C:/Users/Administrator/Desktop/"
    file = "test_data_3.txt"

    # files = glob.glob('*.json')
    savePath = rootPath + "test_data_2.txt"
    sunC = 0
    label_pre = "__label__"
    fsave = open(savePath, 'w', encoding='UTF-8')

    f = open(rootPath+file, 'r', encoding='UTF-8')
    for line in f:
        sentences =  line.strip().split(' ')
        li = sentences[-1]+ " ，" +" ".join(sentences[0:len(sentences)-1])
        sunC +=1
        fsave.writelines(li +"\n")

    fsave.close()
    print("合并后的总数据 = " + str(sunC))
    print("数据保存完成！！！")
    print("\n")



if __name__ == '__main__':
    combine()
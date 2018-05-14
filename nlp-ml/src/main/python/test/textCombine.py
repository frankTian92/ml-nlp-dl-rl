#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/9 0009'
__author__ = 'Administrator'
__filename__ = 'jsonFileTest'
"""
import json

'''
合并json文件
'''


def combine():
    rootPath = "E:/baiduCr/data/DuReader_v2.0_test2/test2set/preprocessed/"
    files = [rootPath + "search.test1.json",
             rootPath + "zhidao.test2.json",
             rootPath + "search.test2.json",
              rootPath + "zhidao.test2.json"]
    # files = glob.glob('*.json')
    savePath = rootPath + "combine.test_1_2.json"
    sunC = 0
    fsave = open(savePath, 'w', encoding='UTF-8')
    for file in files:
        count = 0
        f = open(file, 'r', encoding='UTF-8')
        for line in open(file, 'r', encoding='UTF-8'):
            line = f.readline()
            fsave.writelines(line)
            count += 1
        sunC += count
        print("文件名 = " + file + " 的数量 = " + str(count))
    fsave.close()
    print("合并后的总数据 = " + str(sunC))
    print("数据保存完成！！！")
    print("\n")

    # '''对保存的文件进行验证'''
    with open(savePath, 'r', encoding="UTF-8") as f:
        for lid, line in enumerate(f):
            if lid == 0 or lid == int(sunC / 2) or lid == sunC - 1:
                sample = json.loads(line.strip())
                print(sample['question'])
                print("\n")


if __name__ == '__main__':
    combine()

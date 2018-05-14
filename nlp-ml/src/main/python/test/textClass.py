#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/9 0009'
__author__ = 'Administrator'
__filename__ = 'jsonFileTest'
"""
import glob
import json

'''
合并json文件
'''


def combine():
    rootPath = "E:/baiduCr/data/DuReader_v2.0_preprocess/preprocessed/testset/"
    data_type = ".test1"
    files = [rootPath + "search" + data_type + ".json",
             rootPath + "zhidao" + data_type + ".json"]

    # savePath = rootPath + "combine.json"
    # rootPath = "../"
    # files = glob.glob('*.json')

    question_type = "DESCRIPTION"
    min_type = "_min"
    # question_type = "YES_NO"
    # question_type = "ENTITY"

    savePath = rootPath + question_type.lower() + min_type + data_type + ".json"
    sunC = 0
    fsave = open(savePath, 'w', encoding='UTF-8')
    for file in files:
        count = 0
        f = open(file, 'r', encoding='UTF-8')
        for line in open(file, 'r', encoding='UTF-8'):
            line = f.readline()
            sample = json.loads(line.strip())
            if sample["question_type"] == question_type:
                fsave.writelines(line)
                count += 1
                if count >= 2500:
                    f.close()
                    break
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

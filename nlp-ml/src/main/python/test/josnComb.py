#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/9 0009'
__author__ = 'Administrator'
__filename__ = 'jsonFileTest'
"""
import os
import json

'''
合并json文件
'''


def combine():
    rootPath = "C:/Users/Administrator/Desktop/data/"
    # files = [rootPath + "search.train.json",
    #          rootPath + "zhidao.train.json"]
    # savePath = rootPath + "combine.json"
    # # savePath = "E:/baiduCr/data/DuReader_v2.0_preprocess/preprocessed/devset/" + "combine.dev.json"

    files = os.listdir(rootPath)
    savePath = rootPath + "combine.json"
    except_savePath = rootPath + "except_combine.json"
    except_save = open(except_savePath, 'w', encoding='UTF-8')
    fsave = open(savePath, 'w', encoding='UTF-8')
    sumC = 0
    except_num = 0
    for file in files:
        count = 0
        f = open(rootPath + file, 'r', encoding='UTF-8')
        for line in open(rootPath + file, 'r', encoding='UTF-8'):
            line = f.readline()
            sample = json.loads(line.strip())
            if "fake_answers" in sample and len(sample["fake_answers"])>0:
               if  sample["fake_answers"][0] == "。" or sample["fake_answers"][0] == ".":
                   except_save.writelines(line)
                   except_num += 1
               else:
                   fsave.writelines(line)
                   count += 1
        sumC += count
        print("文件名 = " + file + " 的数量 = " + str(count))
    fsave.close()
    except_save.close()
    print("合并后的总数据 = " + str(sumC))
    print("答案为句号的数量 = " + str(except_num))
    print("数据保存完成！！！")
    print("\n")

    # '''对保存的文件进行验证'''
    with open(savePath, 'r', encoding="UTF-8") as f:
        for lid, line in enumerate(f):
            if lid == 0 or lid == int(sumC / 2) or lid == sumC - 1:
                sample = json.loads(line.strip())
                print(sample['question'])
                print("\n")


if __name__ == '__main__':
    combine()

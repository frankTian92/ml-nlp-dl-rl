#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/9 0009'
__author__ = 'Administrator'
__filename__ = 'classText'
"""

import glob
import json


def classText():
    rootPath = "E:/baiduCr/data/DuReader_v2.0_preprocess/preprocessed/trainset/"
    # rootPath = "../"
    files = [rootPath + "search.train.json",
             rootPath + "zhidao.train.json"]
    # savePath = rootPath + "combine.json"
    # files = glob.glob('*.json')
    # question_type = "DESCRIPTION"
    # question_type = "YES_NO"
    question_type = "ENTITY"
    data_type = ".train"
    savePath = rootPath + question_type.lower() + data_type + ".json"
    result = []
    for file in files:
        count = 0
        with open(file, 'r', encoding='UTF-8') as f:
            for lidx, line in enumerate(f):
                sample = json.loads(line.strip())
                if sample["question_type"] == question_type:
                    result.append(sample)
                    count += 1
                    if count >= 10000:
                        f.close()
                        break
        print(question_type + "文件 = " + file + "  数量 = " + str(count))

    sumC = len(result)
    print('文件名称合并后的总数 = ' + str(sumC))

    '''保存合并的文件'''
    saveFile = open(savePath, "w", encoding="UTF_8")
    json.dump(result, saveFile, ensure_ascii=False)
    saveFile.close()
    print("数据保存完成！！！")
    print("\n")

    # '''对保存的文件进行验证'''
    # with open(savePath, 'r', encoding='UTF-8') as f:
    #     for lid, line in enumerate(f):
    #         if lid == 0 or lid == sumC / 2 or lid == sumC - 1:
    #             sample = json.loads(line.strip())
    #             print(sample['question'])
    #             print("n")


if __name__ == '__main__':
    classText()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/9 0009'
__author__ = 'Administrator'
__filename__ = 'jsonCom'
"""
import glob
import json

'''
合并json文件
'''


def combine():

    readed = json.load(open("E:/baiduCr/data/DuReader_v2.0_preprocess/preprocessed/devset/com/search.dev.json","r",encoding='UTF-8'))
    json.dump(readed, open("E:/baiduCr/data/DuReader_v2.0_preprocess/preprocessed/devset/com/zhidao.dev.json","a",encoding='UTF-8'))
    print("文件合并完成")

    # rootPath = "E:/baiduCr/data/DuReader_v2.0_preprocess/preprocessed/trainset/"
    # files = [rootPath + "search.train.json",
    #          rootPath + "zhidao.train.json"]
    # savePath = rootPath + "combine.json"
    # files = glob.glob('*.json')
    # savePath = "../combine.json"
    # result = []
    # for file in files:
    #     count = 0
    #     with open(file, 'r', encoding='UTF-8') as f:
    #         for lidx, line in enumerate(f):
    #             sample = json.loads(line.strip())
    #             result.append(sample)
    #             count += 1
    #     print("文件 = " + file + "  数量 = " + str(count))
    #
    # sumC = len(result)
    # print('文件名称合并后的总数 = ' + str(sumC))

    '''保存合并的文件'''
    # saveFile = open(savePath, "w", encoding="UTF_8")
    # json.dump(result, saveFile, ensure_ascii=False)
    # saveFile.close()
    # print("数据保存完成！！！")
    # print("\n")

    # '''对保存的文件进行验证'''
    # with open(savePath, 'r', encoding='UTF-8') as f:
    #     for lid, line in enumerate(f):
    #         if lid == 0 or lid == sumC / 2 or lid == sumC - 1:
    #             sample = json.loads(line.strip())
    #             print(sample['question'])
    #             print("n")


if __name__ == '__main__':
    combine()
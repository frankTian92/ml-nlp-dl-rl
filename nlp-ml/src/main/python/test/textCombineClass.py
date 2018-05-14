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
    rootPath = "C:/Users/Administrator/Desktop/"
    files = [rootPath + "test.predicted.description.json",
             rootPath + "test.predicted.entity.json",
             rootPath + "test.predicted.yes.json"]

    # files = glob.glob('*.json')
    savePath = rootPath + "result.json"
    sunC = 0
    fsave = open(savePath, 'w', encoding='UTF-8')
    for file in files:
        count = 0
        i =0
        f = open(file, 'r', encoding='UTF-8')
        for line in open(file, 'r', encoding='UTF-8'):
            line = f.readline()
            sample = json.loads(line.strip())
            if sample["question_type"] == "YES_NO" and sample["answers"]:
                sample["yesno_answers"] = ["Yes"]
                line = json.dumps(sample,ensure_ascii=False)
                i = i+1
                print(i)
                fsave.writelines(line +"\n")
            else:
                fsave.writelines(line)
            count+=1
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
                print(sample['answers'])
                print("\n")


if __name__ == '__main__':
    combine()

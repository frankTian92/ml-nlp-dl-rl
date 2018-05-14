#!/usr/bin/env python


#encoding=utf-8

"""
__mktime__ = '2018/4/22 0022'
__author__ = 'Administrator'
__filename__ = 'testScore'
"""

import json

import sys
import importlib


import sys
import importlib

importlib.reload(sys)
# sys.setdefaultencoding("utf-8")


if __name__ == '__main__':
    rootPath = "E:/baiduCr/DuReader-master/DuReader-master/data/"
    files = rootPath + "combine_utf.train.json"
    f = open(files, 'r',encoding="utf-8")
    SumC = 0
    num =0
    # fsave = open(rootPath+"combine_utf.train.json", 'w',encoding="utf-8")

    # f = open(files,"rb")
    # while True:
    #     line = f.readline()
    #     if not line:
    #         break
    #     else:
    #        try:
    #         #print(line.decode('utf8'))
    #         li =  line.decode('utf8')
    #         SumC +=1
    #         print(str(SumC))
    #         fsave.writelines(li)
    #         #为了暴露出错误，最好此处不print
    #        except:
    #            num+=1
    #            print("出问题的个数 = " +str(num))

    for line in open(files, 'r',encoding="utf-8"):
            SumC +=1
            li = f.readline()
            sample = json.loads(li)
            if sample["question"] in ["鸟屎掉衣服上吉不吉利"] :
                print()
            li = json.dumps(sample,ensure_ascii=False)
            print(str(SumC))


    print( "总共文章个数 = " + str(SumC))
    # fsave.close()
    f.close()

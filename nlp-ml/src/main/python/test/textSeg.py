# -*- coding: UTF-8 -*-
"""
__mktime__ = '2018/4/9 0009'
__author__ = 'Administrator'
__filename__ = 'jsonFileTest'
"""
from io import open


'''
分开json文件
'''
def seg():
    rootPath = "E:/baiduCr/DuReader-master/DuReader-master/data/demo/devset/"
    file = rootPath+ "search.dev.json"
    # files = glob.glob('*.json')
    count = 0
    batch_size =10
    batch_num =0

    fsave = open( rootPath + "seg.train_0.json", 'w', encoding='UTF-8')

    f = open(file, 'r', encoding='UTF-8')
    for line in open(file, 'r', encoding='UTF-8'):
        line = f.readline()
        if count % batch_size == 0 and count>0:
            batch_num += 1
            print("已保存数据量 = " +str(count))
            print("保存的文件名 = " + (rootPath + "seg.train_"+str(batch_num)+".json"))
            fsave.close()
            fsave = open(rootPath + "seg.train_"+str(batch_num)+".json", 'w', encoding='UTF-8')
        fsave.writelines(line)
        count += 1


    fsave.close()


if __name__ == '__main__':
    seg()

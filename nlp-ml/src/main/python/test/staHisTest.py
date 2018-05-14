#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/18 0018'
__author__ = 'Administrator'
__filename__ = 'staHis'
词长统计及汇制分布图
"""
import json
import matplotlib.pyplot as plot
import numpy as np


def statistics():
    rootPath = "E:/baiduCr/data/DuReader_v2.0_preprocess/preprocessed/"
    files = [rootPath + "testset/combine.test1.json"]

    saveRootPath = "E:/baiduCr/static/test/"
    savePath = "E:/baiduCr/static/test/"

    more_than_para_length_save = open(savePath + "more_than_para_length_1800.json", 'w', encoding='UTF-8')
    more_than_para_length_seg_save = open(savePath + " more_than_para_length_seg_1200.json", 'w', encoding='UTF-8')
    more_than_seg_question_length_save = open(savePath + "most_than_seg_question_30.json", 'w', encoding='UTF-8')
    more_than_para_distence_num_save = open(savePath + "more_than_para_distence_num_40.json", 'w', encoding='UTF-8')

    more_than_para_Length = 1800
    more_than_para_seg_Length = 1200
    most_than_seg_question_Length = 30
    more_than_para_distence_num = 40

    m_p_l = []
    m_p_s = []
    m_q_s = []
    m_p_d = []

    # 句子分词之后的长度统计
    test_paragraphs_seg_length_dict = {}
    test_paragraphs_seg_length_list = []

    # 句子未分词的长度统计
    test_paragraphs_length_dict = {}
    test_paragraphs_length_list = []

    # 问题分词未分词的长度统计
    test_paragraphs_num_dict = {}
    test_paragraphs_num_list = []

    # 问题分词的长度统计
    test_question_seg_length_dict = {}
    test_question_seg_length_list = []

    # 问题分词未分词的长度统计
    test_question_length_dict = {}
    test_question_length_list = []

    for file in files:
        f = open(file, 'r', encoding='UTF-8')
        for line in open(file, 'r', encoding='UTF-8'):
            line = f.readline()
            sample = json.loads(line.strip())
            if len(sample["question"]) == 0:
                continue

            makeDict(dict=test_question_length_dict, lists=test_question_length_list, file_name="question",
                     sample=sample, cetagery=1,
                     savePtah=None, max_v=None, raw_sample=None, datas=None)
            makeDict(dict=test_question_seg_length_dict, lists=test_question_seg_length_list,
                     file_name="segmented_question", sample=sample, cetagery=1,
                     savePtah=more_than_seg_question_length_save, max_v=most_than_seg_question_Length,
                     raw_sample=line, datas=m_q_s)

            for d_idx, doc in enumerate(sample['documents']):
                makeDict(dict=test_paragraphs_length_dict, lists=test_paragraphs_length_list,
                         file_name="paragraphs", sample=doc, cetagery=2,
                         savePtah=more_than_para_length_save, max_v=more_than_para_Length,
                         raw_sample=line, datas=m_p_l)
                makeDict(dict=test_paragraphs_seg_length_dict, lists=test_paragraphs_seg_length_list,
                         file_name="segmented_paragraphs", sample=doc, cetagery=2,
                         savePtah=more_than_para_length_seg_save, max_v=more_than_para_seg_Length,
                         raw_sample=line, datas=m_p_s)
                makeDict(dict=test_paragraphs_num_dict, lists=test_paragraphs_num_list,
                         file_name="paragraphs", sample=doc, cetagery=1,
                         savePtah=more_than_para_distence_num_save, max_v=more_than_para_distence_num,
                         raw_sample=line, datas=m_p_d)

        f.close()

    # items1 = saveDict(saveRootPath + "dict/", "test_paragraphs_seg_length_dict.txt", test_paragraphs_seg_length_dict)
    # transform_save_data(saveRootPath, "test_paragraphs_seg_length_dict.txt", items1)
    # plotbarn(lists=test_paragraphs_seg_length_list, x_name="test_paragraphs_seg_length",
    #          title="test_paragraphs_seg_length",
    #          rootPath=saveRootPath, png_name="test_paragraphs_seg_length.png")
    #
    # items2 = saveDict(saveRootPath + "dict/", "test_paragraphs_length_dict.txt", test_paragraphs_length_dict)
    # transform_save_data(saveRootPath, "test_paragraphs_length_dict.txt", items2)
    # plotbarn(lists=test_paragraphs_length_list, x_name="test_paragraphs_length", title="test_paragraphs_length",
    #          rootPath=saveRootPath,
    #          png_name="test_paragraphs_length.png")
    #
    # items3 = saveDict(saveRootPath + "dict/", "test_question_seg_length_dict.txt", test_question_seg_length_dict)
    # transform_save_data(saveRootPath, "test_question_seg_length_dict.txt", items3)
    # plotbarn(lists=test_question_seg_length_list, x_name="test_question_seg_length", title="test_question_seg_length",
    #          rootPath=saveRootPath, png_name="test_question_seg_length.png")
    #
    # items4 = saveDict(saveRootPath + "dict/", "test_question_length_dict.txt", test_question_length_dict)
    # transform_save_data(saveRootPath, "test_question_length_dict.txt", items4)
    # plotbarn(lists=test_question_length_list, x_name="test_question_length", title="test_question_length",
    #          rootPath=saveRootPath,
    #          png_name="test_question_length.png")
    #
    # items5 = saveDict(saveRootPath + "dict/", "test_paragraphs_num_dict.txt", test_paragraphs_num_dict)
    # transform_save_data(saveRootPath, "test_paragraphs_num_dict.txt", items5)
    # plotbarn(lists=test_paragraphs_num_list, x_name="test_paragraphs_num", title="test_paragraphs_num",
    #          rootPath=saveRootPath,
    #          png_name="test_paragraphs_num.png")
    #
    # more_than_seg_question_length_save.close()
    # more_than_para_distence_num_save.close()
    # more_than_para_length_save.close()
    # more_than_para_length_seg_save.close()

    # fsave.close()


'''
统计长度
'''


def makeDict(dict, lists, file_name, sample, cetagery, savePtah, max_v, raw_sample, datas):
    if file_name is None:
        lens = len(sample)
        if lens in dict.keys():
            dict[lens] = dict[lens] + 1
        else:
            dict[lens] = 1
        lists.append(lens)
    else:
        if type(sample[file_name]) == list:
            if cetagery == 1:
                f_sample = sample[file_name]
                lens = len(f_sample)
                if lens==0:
                    print(f_sample)
                if max_v is not None:
                    if lens > max_v:
                        if raw_sample not in datas:
                            datas.append(raw_sample)
                            savePtah.writelines(raw_sample)
                if lens in dict.keys():
                    dict[lens] = dict[lens] + 1
                else:
                    dict[lens] = 1
                lists.append(lens)

            if cetagery == 2:
                f_sample = sample[file_name]
                for s_sample in f_sample:
                    lens = len(s_sample)
                    if lens==0:
                         print(s_sample)
                    if max_v is not None:
                        if lens > max_v:
                            if raw_sample not in datas:
                                datas.append(raw_sample)
                                savePtah.writelines(raw_sample)
                    if lens in dict.keys():
                        dict[lens] = dict[lens] + 1
                    else:
                        dict[lens] = 1
                    lists.append(lens)
        else:
            lens = len(sample[file_name])
            if lens in dict.keys():
                dict[lens] = dict[lens] + 1
            else:
                dict[lens] = 1
            lists.append(lens)


def makeNumDict(dict, lists, num):
    if num in dict.keys():
        dict[num] = dict[num] + 1
    else:
        dict[num] = 1
    lists.append(num)


def saveDict(path, file_name, dict):
    f = open(path + file_name, "w")
    items = dict.items()
    m = sorted(items, key=lambda item: item[0])
    f.write(str(m))
    f.close()
    return m


def readDict(path, file_name, dict):
    f = open(path + file_name, "r")
    a = f.read()
    data = eval(a)
    f.close()
    return data


def transform_save_data(saveRootPath, file_name, items):
    words = []
    counts = []
    f = open(saveRootPath + "list/" + file_name, "w")
    for word, count in items:
        words.append(word)
        counts.append(count)
    f.writelines(str(words) + "\n")
    f.writelines(str(counts))
    f.close()


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
    plot.savefig(fname=rootPath + "bar/" + png_name, format='png')


if __name__ == '__main__':
    statistics()

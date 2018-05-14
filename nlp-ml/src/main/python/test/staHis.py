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
    files = [rootPath + "devset/combine.dev.json",
             rootPath + "trainset/combine.train.json"]

    saveRootPath = "E:/baiduCr/static/"

    # 句子分词之后的长度统计
    paragraphs_seg_length_dict = {}
    paragraphs_seg_length_list = []

    # 句子未分词的长度统计
    paragraphs_length_dict = {}
    paragraphs_length_list = []

    # 问题分词的长度统计
    question_seg_length_dict = {}
    question_seg_length_list = []

    # 问题分词未分词的长度统计
    question_length_dict = {}
    question_length_list = []

    # 标准答案的分词统计
    answer_seg_length_dict = {}
    answer_seg_length_list = []

    # 标准答案未分词的统计
    answer_length_dict = {}
    answer_length_list = []

    # 与答案相关的段落统计
    most_related_para_dict = {}
    most_related_para_list = []

    # 计算出的答案长度
    fake_answer_lenth = {}
    fake_answer_length_list = []

    # 计算答案的开始位置
    answer_spans_start = {}
    answer_spans_start_list = []

    # 计算答案的末端位置
    answer_spans_end = {}
    answer_spans_end_list = []

    # 计算fake——answer与标准答案的匹配度得分
    match_scores = {}
    match_scores_list = []

    #计算答案直接的跨度
    answer_spans_distant_dict = {}
    answer_spans_distant_list =[]

    for file in files:
        f = open(file, 'r', encoding='UTF-8')
        for line in open(file, 'r', encoding='UTF-8'):
            line = f.readline()
            sample = json.loads(line.strip())
            if len(sample['answer_spans']) == 0:
                continue
            # fake_answers
            # makeDict(dict=fake_answer_lenth, lists=fake_answer_length_list, file_name="fake_answers", sample=sample)
            # makeDict(dict=question_length_dict, lists=question_length_list, file_name="question", sample=sample)
            # makeDict(dict=question_seg_length_dict, lists=question_seg_length_list, file_name="segmented_question",
            #          sample=sample)
            #
            # for answer_list in sample["answers"]:
            #     makeDict(dict=answer_length_dict, lists=answer_length_list, file_name=None, sample=answer_list)
            #
            # for answer_seg_list in sample["segmented_answers"]:
            #     makeDict(dict=answer_seg_length_dict, lists=answer_seg_length_list, file_name=None,
            #              sample=answer_seg_list)
            #
            # for d_idx, doc in enumerate(sample['documents']):
            #     if doc["is_selected"]:
            #         most_related_para = doc['most_related_para']
            #         makeNumDict(dict=most_related_para_dict, lists=most_related_para_list, num=most_related_para)
            #
            #         para_seg = doc['segmented_paragraphs'][most_related_para]
            #         makeDict(dict=paragraphs_seg_length_dict, lists=paragraphs_seg_length_list, file_name=None,
            #                  sample=para_seg)
            #
            #         para = doc['paragraphs'][most_related_para]
            #         makeDict(dict=paragraphs_length_dict, lists=paragraphs_length_list, file_name=None, sample=para)

            if sample["answer_spans"]:
                answer_spans = sample["answer_spans"]
                # makeNumDict(dict=answer_spans_start, lists=answer_spans_start_list, num=answer_spans[0][0])
                #
                # makeNumDict(dict=answer_spans_end, lists=answer_spans_end_list, num=answer_spans[0][1])
                distance = answer_spans[0][1]-answer_spans[0][0]
                makeNumDict(dict=answer_spans_distant_dict,lists=answer_spans_distant_list,num= distance)

                # makeNumDict(dict=match_scores, lists=match_scores_list, num=round(sample["match_scores"][0], 2))

        f.close()

    # items1 = saveDict(saveRootPath + "dict/", "paragraphs_seg_length_dict.txt", paragraphs_seg_length_dict)
    # transform_save_data(saveRootPath, "paragraphs_seg_length_dict.txt", items1)
    # plotbarn(lists=paragraphs_seg_length_list, x_name="paragraphs_seg_length", title="paragraphs_seg_length",
    #          rootPath=saveRootPath, png_name="paragraphs_seg_length.png")
    #
    # items2 = saveDict(saveRootPath + "dict/", "paragraphs_length_dict.txt", paragraphs_length_dict)
    # transform_save_data(saveRootPath, "paragraphs_length_dict.txt", items2)
    # plotbarn(lists=paragraphs_length_list, x_name="paragraphs_length", title="paragraphs_length", rootPath=saveRootPath,
    #          png_name="paragraphs_length.png")
    #
    # items3 = saveDict(saveRootPath + "dict/", "question_seg_length_dict.txt", question_seg_length_dict)
    # transform_save_data(saveRootPath, "question_seg_length_dict.txt", items3)
    # plotbarn(lists=question_seg_length_list, x_name="question_seg_length", title="question_seg_length",
    #          rootPath=saveRootPath, png_name="question_seg_length.png")
    #
    # items4 = saveDict(saveRootPath + "dict/", "question_length_dict.txt", question_length_dict)
    # transform_save_data(saveRootPath, "question_length_dict.txt", items4)
    # plotbarn(lists=question_length_list, x_name="question_length", title="question_length", rootPath=saveRootPath,
    #          png_name="question_length.png")
    #
    # items5 = saveDict(saveRootPath + "dict/", "answer_seg_length_dict.txt", answer_seg_length_dict)
    # transform_save_data(saveRootPath, "answer_seg_length_dict.txt", items5)
    # plotbarn(lists=answer_seg_length_list, x_name="answer_seg_length", title="answer_seg_length", rootPath=saveRootPath,
    #          png_name="answer_seg_length.png")
    #
    # items6 = saveDict(saveRootPath + "dict/", "answer_length_dict.txt", answer_length_dict)
    # transform_save_data(saveRootPath, "answer_length_dict.txt", items6)
    # plotbarn(lists=answer_length_list, x_name="answer_length", title="answer_length", rootPath=saveRootPath,
    #          png_name="answer_length.png")
    #
    # items7 = saveDict(saveRootPath + "dict/", "most_related_para_dict.txt", most_related_para_dict)
    # transform_save_data(saveRootPath, "most_related_para_dict.txt", items7)
    # plotbarn(lists=most_related_para_list, x_name="most_related_para_num", title="most_related_para_num",
    #          rootPath=saveRootPath, png_name="most_related_para.png")
    #
    # items8 = saveDict(saveRootPath + "dict/", "fake_answer_length.txt", fake_answer_lenth)
    # transform_save_data(saveRootPath, "fake_answer_length.txt", items8)
    # plotbarn(lists=fake_answer_length_list, x_name="fake_answer_length", title="fake_answer_length",
    #          rootPath=saveRootPath, png_name="fake_answer_length.png")
    #
    # items9 = saveDict(saveRootPath + "dict/", "answer_spans_start.txt", answer_spans_start)
    # transform_save_data(saveRootPath, "answer_spans_start.txt", items9)
    # plotbarn(lists=answer_spans_start_list, x_name="answer_spans_start_index", title="answer_spans_start",
    #          rootPath=saveRootPath, png_name="answer_spans_start.png")
    #
    # items10 = saveDict(saveRootPath + "dict/", "answer_spans_end.txt", answer_spans_end)
    # transform_save_data(saveRootPath, "answer_spans_end.txt", items10)
    # plotbarn(lists=answer_spans_end_list, x_name="answer_spans_end_index", title="answer_spans_end",
    #          rootPath=saveRootPath, png_name="answer_spans_end.png")
    #
    # items11 = saveDict(saveRootPath + "dict/", "match_scores.txt", match_scores)
    # transform_save_data(saveRootPath, "match_scores.txt", items11)
    # plotbarn(lists=match_scores_list, x_name="match_scores", title="match_scores", rootPath=saveRootPath,
    #          png_name="match_scores.png")

    items12 = saveDict(saveRootPath + "dict/", "answer_spans_distant_dict.txt", answer_spans_distant_dict)
    transform_save_data(saveRootPath, "answer_spans_distant.txt", items12)
    plotbarn(lists=answer_spans_distant_list, x_name="answer_spans_distant", title="answer_spans_distant", rootPath=saveRootPath,
             png_name="answer_spans_distant.png")


    # fsave.close()


'''
统计长度
'''


def makeDict(dict, lists, file_name, sample):
    if file_name is None:
        lens = len(sample)
        if lens in dict.keys():
            dict[lens] = dict[lens] + 1
        else:
            dict[lens] = 1
        lists.append(lens)
    else:
        if type(sample[file_name]) == list:
            for sme  in sample[file_name]:
                lens = len(sme)
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

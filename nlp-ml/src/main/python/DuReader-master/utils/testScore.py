#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/22 0022'
__author__ = 'Administrator'
__filename__ = 'testScore'
"""

import json
import numpy as np

if __name__ == '__main__':
    data_path ="home/huwei/baiduCr/data/preprocess/trainset/combine_clean.train.json"

    with open(data_path, 'r', encoding='UTF-8') as fin:

        for lidx, line in enumerate(fin):
            sample = json.loads(line.strip())
            if len(sample['answer_spans']) == 0:
                continue
            if sample['answer_spans'][0][1] >= 500:
                continue
            print("qusitonsId = " +sample["question_id"])
            if 'answer_docs' in sample:
                sample['answer_passages'] = sample['answer_docs']
                print("answer_passages = " + sample['answer_docs'][0])
                print("answer_spans = [" + sample["answer_spans"][0] + "," +sample["answer_spans"])


            print("question = "+sample['segmented_question'][0])

            sample['passages'] = []
            for d_idx, doc in enumerate(sample['documents']):
                 most_related_para = doc['most_related_para']
                 print("most_related_para = "+ most_related_para)
                 print("passage_tokens = " + "".join(doc['segmented_paragraphs'][most_related_para]))

            print("__________________________")
            print("\n")

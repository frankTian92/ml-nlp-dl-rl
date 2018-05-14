###############################################################################
# ==============================================================================
# Copyright 2017 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""
This module finds the most related paragraph of each document according to recall.
"""
# -*- coding: utf-8 -*-

import sys
import importlib
import math

if sys.version[0] == '3':
    importlib.reload(sys)
    # sys.setdefaultencoding("utf-8")
import json



def find_fake_answer(sample):
    """
    For each document, finds the most related paragraph based on recall,
    then finds a span that maximize the f1_score compared with the gold answers
    and uses this span as a fake answer span
    Args:
        sample: a sample in the dataset
    Returns:
        None
    Raises:
        None
    """
    if  "answer_docs" in sample :
        answer_docs = sample["answer_docs"]
        documents = sample['documents']

        if len(answer_docs)>0:
           answer_doc = documents[answer_docs[0]]
           most_related_para_tokens = answer_doc["most_related_para"]
           paragraphs = answer_doc["segmented_paragraphs"]
           most_related_para = paragraphs[most_related_para_tokens]
           start_id = sample["answer_spans"][0][0]
           end_id = sample["answer_spans"][0][1]

           print("计算得到的最相关答案= ","".join(most_related_para[start_id:end_id+1] ))
           print("最终得到的最相关答案 = " + "".join(sample["fake_answers"][0]))
           if sample["fake_answers"][0] =="。" or sample["fake_answers"][0] ==".":
               print("。。。。。。。。。。。。")
           print("---------------------------")



if __name__ == '__main__':
    rootPath = "C:/Users/Administrator/Desktop/"
    files = rootPath + "fix_train_0.json"
    # savePath = rootPath + "search.train.fixed.json"
    f = open(files, 'r', encoding='UTF-8')
    num = 0
    for line in open(files, 'r', encoding='UTF-8'):
        li = f.readline()
        sample = json.loads(li)
        find_fake_answer(sample)

    f.close()
    # print(json.dumps(sample, encoding='utf8', ensure_ascii=False))

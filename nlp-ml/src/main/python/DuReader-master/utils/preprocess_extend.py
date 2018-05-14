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


if sys.version[0] == '2':
    importlib.reload(sys)
    sys.setdefaultencoding("utf-8")
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
    if "answer_docs" in sample and len(sample["answer_docs"])==1:

        # 对其他段落中的文章进行扩展
        for doc_id, doc in enumerate(sample["documents"]):
            most_related_para = doc["most_related_para"]
            most_segmented_paragraphs = doc["segmented_paragraphs"][most_related_para]
            doc["segmented_paragraphs"] = [most_segmented_paragraphs]
            doc["paragraphs"]=[]
            doc["most_related_para"] =0
        sample["question"]=""
        sample["fake_answers"] =""
        sample["fact_or_opinion"]=""




if __name__ == '__main__':
    rootPath = "C:/Users/Administrator/Desktop/"
    files = rootPath + "test.predicted.yesno.json"
    savePath = rootPath + "fix_train_0.extend.json"
    f = open(files, 'r', encoding='UTF-8')
    fsave = open(savePath, 'w', encoding='UTF-8')
    num = 0
    for line in open(files, 'r', encoding='UTF-8'):
        li = f.readline()

        #扩展数据
        sample = json.loads(li)
        find_fake_answer(sample)
        li = json.dumps(sample, ensure_ascii=False)
        fsave.writelines(li + "\n")
        num+=1
    print("共有数据  = "+str(num))
    f.close()

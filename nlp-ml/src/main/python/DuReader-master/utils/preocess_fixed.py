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
from io import open
import json

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")
import json


def get_dict_raw_samlpe(raw_sample_fliePath):
    raw_sample_dict = {}
    f = open(raw_sample_fliePath, 'r', encoding='UTF-8')
    for line in open(raw_sample_fliePath, 'r', encoding='UTF-8'):
        li = f.readline()
        sample = json.loads(li)
        question_id = sample["question_id"]
        raw_sample_dict[question_id] = sample
    f.close()
    return raw_sample_dict


def fixed_fake_answer(sample, raw_samples_dict):
    question_id = sample["question_id"]
    if "fake_answers" in sample and len(sample["fake_answers"]) > 0:
        if sample["fake_answers"][0] == "。" or sample["fake_answers"][0] == ".":
            raw_sample = raw_samples_dict[question_id]
            if "match_scores" in raw_sample and len(raw_sample["match_scores"]) > 0:
                match_scores_raw = raw_sample["match_scores"][0]
                if match_scores_raw >= 0.20:
                    print("原来的答案 = " + sample["fake_answers"][0])
                    print("现在的答案  = " + raw_sample["fake_answers"][0])
                    print("---------------")
                    sample = raw_sample
    return sample


if __name__ == '__main__':
    arg = sys.argv
    file_name = arg[1]
    raw_Path = "/home/huwei/baiduCr/data/preprocess/data/data_seg/"
    fix_Path = "/home/huwei/baiduCr/data/preprocess/data/data_fix/"
    save_Path = "/home/huwei/baiduCr/data/preprocess/data/data_seg_fix/"

    raw_file = raw_Path + "seg.train_" + file_name + ".json"
    fix_file = fix_Path + "fix_train_" + file_name + ".json"
    save_file = save_Path + "seg_fix_train_" + file_name + ".json"

    fsave = open(save_file, 'w', encoding='UTF-8')

    num = 0
    save_num = 0
    raw_sample_dict = get_dict_raw_samlpe(raw_file)

    f = open(fix_file, 'r', encoding='UTF-8')
    for line in open(fix_file, 'r', encoding='UTF-8'):
        li = f.readline()
        sample = json.loads(li)
        sample = fixed_fake_answer(sample=sample, raw_samples_dict=raw_sample_dict)
        li = json.dumps(sample, ensure_ascii=False)
        fsave.writelines(li + "\n")
        save_num += 1

        num += 1
        print(num)
    print("数据总量 = " + str(num))
    print("被遗弃的数据量 = " + str(num - save_num))
    print("保存的数据量 = " + str(save_num))
    f.close()
    fsave.close()

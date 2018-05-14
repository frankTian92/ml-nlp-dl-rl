#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/11 0011'
__author__ = 'Administrator'
__filename__ = 'vocabLoad'
"""

import os
import pickle
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
def loadvocab(path):
     with open(os.path.join(path, 'vocab.data'), 'rb') as fin:
          vocab = pickle.load(fin)
     max =  vocab.max()

     print(max)





if __name__ == '__main__':
    loadvocab("E:/baiduCr/DuReader-master/DuReader-master/data/vocab/")
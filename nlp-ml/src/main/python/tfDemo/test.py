#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/5/21 0021'
__author__ = 'Administrator'
__filename__ = 'test'
"""


import numpy as np
import tensorflow as tf

var = tf.one_hot(indices=[1,2,3], depth=4, axis=0)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    a = sess.run(var)
    print(a)



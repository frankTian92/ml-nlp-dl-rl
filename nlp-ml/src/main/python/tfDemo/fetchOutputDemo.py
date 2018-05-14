#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/17 0017'
__author__ = 'Administrator'
__filename__ = 'tffetchMulValueDemo'
"""
'''
fetch：取多值的例子,输出多个值
'''
import tensorflow as tf

input1 = tf.constant(3.0)
input2 = tf.constant(2.0)
input3 = tf.constant(5.0)
intermed = tf.add(input2, input3)
mull = tf.mul(input1, intermed)

with tf.Session() as sess:
    result = sess.run([mull, intermed])
    print(result)
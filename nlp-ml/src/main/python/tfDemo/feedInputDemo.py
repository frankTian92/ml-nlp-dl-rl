#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/17 0017'
__author__ = 'Administrator'
__filename__ = 'feedInputDemo'
"""

'''
feed : 输入
'''
import tensorflow as tf
input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)
output = tf.add(input1,input2)

with tf.Session() as sess:
    print(sess.run([output],feed_dict={
        input1: [7.0],
        input2: [2.0]
    }))

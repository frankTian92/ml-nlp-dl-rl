#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/17 0017'
__author__ = 'Administrator'
__filename__ = 'tfCount'
"""
import tensorflow as tf
state = tf.Variable(0, name="counter")
one = tf.constant(1)
new_value = tf.add(state, one)

update = tf.assign(state,new_value)

init_op = tf.initialize_all_variables()

with tf.Session() as sess:
    sess.run(init_op)
    print(sess.run(state))
    for _ in range(3):
        sess.run(update)
        print(sess.run(state))
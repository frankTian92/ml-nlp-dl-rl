#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/14 0014'
__author__ = 'Administrator'
__filename__ = 'nolinRegTest'
"""
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.python import debug as tf_debug

x_data = np.linspace(-0.5, 0.5, 20)[:, np.newaxis]
noise = np.random.normal(0.0, 0.2, x_data.shape)
y_data = np.square(x_data) + noise

x = tf.placeholder(tf.float32, [None, None])
y = tf.placeholder(tf.float32, [None, None])

Weights_L1 = tf.Variable(tf.random_normal([1, 1]))
b_L1 = tf.Variable(tf.zeros([1, 1]))
Wx_plus_b_L1 = tf.matmul(x, Weights_L1) + b_L1
L1 = tf.nn.tanh(Wx_plus_b_L1)

Weights_L2 = tf.Variable(tf.random_normal([1, 1]))
b_L2 = tf.Variable(tf.zeros([1, 1]))
Wx_plus_b_L2 = tf.matmul(L1, Weights_L2) + b_L2
prediction = tf.nn.tanh(Wx_plus_b_L2)

loss = tf.reduce_mean(tf.square(y - prediction))

train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

with tf.Session() as sess:
    # sess = tf_debug.TensorBoardDebugWrapperSession(sess, "SC-201712291455:6064")
    sess.run(tf.global_variables_initializer())
    for _ in range(2000):
        sess.run(train_step, feed_dict={x: x_data, y: y_data})

    prediction_v = sess.run(prediction, feed_dict={x: x_data})

    # plt.figure()
    # plt.scatter(x_data, y_data)
    # plt.plot(x_data, prediction_v, 'r-', lw=5)
    # plt.show()

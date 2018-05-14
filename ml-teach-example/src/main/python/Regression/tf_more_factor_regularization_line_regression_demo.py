#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/5/4 0004'
__author__ = 'Administrator'
__filename__ = 'tf_line_regression_demo'
广告点击量与广告投入的线性回归
"""

from __future__ import print_function
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

rng = np.random

# 参数
learning_rate = 0.000000002
training_epochs = 200000
display_step = 100

# 分类数据
train_X_outdoor = np.asarray(
    [[38.4, 56, 2.31, 0.34], [36.6, 54, 1.67, 0.29], [35.3, 55, 1.94, 0.3], [33.8, 51, 1.73, 0.31],
     [24.2, 45, 1.44, 0.27], [12.9, 35, 2.07, 0.35], [1, 10, 0.92, 0.25], [2.5, 14, 2.72, 0.37], [2.4, 13, 2.07, 0.32],
     [16.1, 35, 1.45, 0.31], [11.4, 31, 1.58, 0.26], [33.3, 52, 1.85, 0.3], [13.2, 33, 1.63, 0.28], [6, 21, 1.67, 0.3],
     [4.2, 19, 2.01, 0.3], [9.1, 29, 2.68, 0.35], [13.9, 34, 1.76, 0.31], [33, 48, 1.62, 0.29], [32.8, 48, 1.62, 0.3],
     [17.6, 35, 1.81, 0.29], [9.7, 30, 1.95, 0.31], [7.4, 24, 0.78, 0.26], [12.7, 32, 2.33, 0.34],
     [7.8, 26, 2.11, 0.32], [24, 41, 2.53, 0.33], [27.6, 48, 0.87, 0.24], [20.7, 41, 1.19, 0.26],
     [17.6, 35, 1.68, 0.31], [31.6, 47, 1.71, 0.27], [30.5, 53, 2.04, 0.32], [30.4, 46, 1.99, 0.31],
     [24.2, 43, 2.09, 0.34], [25, 42, 0.95, 0.26]])
train_Y_outdoor = np.asarray(
    [69.4, 66.9, 65.9, 64, 45.7, 24.3, 1.5, 4.7, 4.7, 30.5, 21.3, 63.3, 24.7, 11.3, 7.9, 17.3, 26.5, 62.4, 61.9, 32.7,
     18.1, 14.1, 24.1, 14.6, 44.8, 53, 39.3, 33.5, 59.4, 56.7, 57.9, 45.9, 47.1])

train_X_tv = np.asarray([[16.9, 45, 3.38, 0.29], [1.5, 15, 3.27, 0.28], [2.5, 17, 3.11, 0.29], [22.2, 48, 2.93, 0.29],
                         [25.1, 56, 4.51, 0.34], [13.9, 46, 4.5, 0.32], [4.5, 27, 2.55, 0.29], [12.9, 45, 4.01, 0.34],
                         [20, 49, 2.62, 0.27],
                         [17.9, 47, 3.95, 0.35], [10.4, 36, 3.48, 0.31], [14.4, 48, 2.6, 0.29], [15.7, 49, 2.05, 0.28],
                         [10.6, 39, 5.31, 0.39], [20.3, 52, 3.54, 0.3], [1.6, 13, 2.68, 0.26]])
train_Y_tv = np.asarray([18.5, 1.6, 2.7, 24.5, 27.2, 15.1, 4.9, 14.0, 21.7, 19.3, 11.3, 15.7, 17.2, 11.5, 21.9, 1.8])

train_X_broadcast = np.asarray(
    [[13.6, 44, 4.68, 0.35], [23.1, 62, 3.8, 0.32], [4.3, 26, 2.68, 0.28], [14, 49, 2.7, 0.3], [20.8, 53, 2.24, 0.29],
     [12.8, 46, 1.69, 0.24], [18.6, 56, 3.14, 0.27]])
train_Y_broadcast = np.asarray([15, 24.8, 4.6, 15.1, 22.6, 13.7, 20])

train_X_internet = np.asarray(
    [[61.9, 74, 2.87, 0.2], [50, 64, 5.11, 0.26], [60.6, 74, 10.42, 0.38], [54.8, 66, 6.87, 0.32]])
train_Y_internet = np.asarray([164.6, 125.3, 159.1, 136.2])

# 获取样本个数
n_samples_outdoor = train_Y_outdoor.shape[0]
n_samples_tv = train_Y_tv.shape[0]
n_samples_broadcast = train_Y_broadcast.shape[0]
n_samples_internet = train_Y_internet.shape[0]

# 定义模型的输入和输出
X_outdoor = tf.placeholder("float")
Y_outdoor = tf.placeholder("float")
X_tv = tf.placeholder("float")
Y_tv = tf.placeholder("float")
X_broadcast = tf.placeholder("float")
Y_broadcast = tf.placeholder("float")
X_internet = tf.placeholder("float")
Y_internet = tf.placeholder("float")
X_exposure = tf.placeholder("float")
X_quality = tf.placeholder("float")
X_time = tf.placeholder("float")

# 设置模型的参数
W_outdoor = tf.Variable(rng.randn(), name="weight_outdoor")
W_outdoor_5 = tf.Variable(rng.randn(), name="weight_outdoor_5")
b_outdoor = tf.Variable(rng.randn(), name="bias_outdoor")

W_tv = tf.Variable(rng.randn(), name="weight_tv")
W_tv_5 = tf.Variable(rng.randn(), name="weight_tv_5")
b_tv = tf.Variable(rng.randn(), name="bias_tv")

W_broadcast = tf.Variable(rng.randn(), name="weight_broadcast")
W_broadcast_5 = tf.Variable(rng.randn(), name="weight_broadcast_5")
b_broadcast = tf.Variable(rng.randn(), name="bias_broadcast")

W_internet = tf.Variable(rng.randn(), name="weight_internet")
W_internet_5 = tf.Variable(rng.randn(), name="weight_internet_5")
b_internet = tf.Variable(rng.randn(), name="bias_internet")

W_exposure_1 = tf.Variable(rng.randn(), name="weight_exposure_1")
W_exposure_2 = tf.Variable(rng.randn(), name="weight_exposure_2")

W_quality_1 = tf.Variable(rng.randn(), name="weight_quality_1")
W_quality_2 = tf.Variable(rng.randn(), name="weight_quality_2")

W_time_1 = tf.Variable(rng.randn(), name="weight_time_1")
W_time_2 = tf.Variable(rng.randn(), name="weight_time_2")

λ = 10

# 构造线性模型

pred_exposure = tf.add(tf.multiply(X_exposure, W_exposure_1), tf.multiply(tf.square(X_exposure), W_exposure_2))
pred_quality = tf.add(tf.multiply(X_quality, W_quality_1), tf.multiply(tf.square(X_quality), W_quality_2))
pred_time = tf.add(tf.multiply(X_time, W_time_1), tf.multiply(tf.square(X_time), W_time_2))
pred_other_sum = pred_exposure + pred_quality + pred_time

pred_outdoor = tf.add(tf.multiply(X_outdoor, W_outdoor), b_outdoor)
pred_outdoor = tf.add(tf.multiply(tf.square(X_outdoor), W_outdoor_5), pred_outdoor)

pred_tv = tf.add(tf.multiply(X_tv, W_tv), b_tv)
pred_tv = tf.add(tf.multiply(tf.square(X_tv), W_tv_5), pred_tv)

pred_broadcast = tf.add(tf.multiply(X_broadcast, W_broadcast), b_broadcast)
pred_broadcast = tf.add(tf.multiply(tf.square(X_broadcast), W_broadcast_5), pred_broadcast)

pred_internet = tf.add(tf.multiply(X_internet, W_internet), b_internet)
pred_internet = tf.add(tf.multiply(tf.square(X_internet), W_internet_5), pred_internet)

# 定义损失函数——均方误差（MSE——mean squared error）

loss_outdoor = tf.reduce_sum(tf.pow(pred_outdoor + pred_other_sum - Y_outdoor, 2)) / (n_samples_outdoor)
loss_tv = tf.reduce_sum(tf.pow(pred_tv + pred_other_sum - Y_tv, 2)) / (n_samples_tv)
loss_broadcast = tf.reduce_sum(tf.pow(pred_broadcast + pred_other_sum - Y_broadcast, 2)) / (n_samples_broadcast)
loss_internet = tf.reduce_sum(tf.pow(pred_internet + pred_other_sum - Y_internet, 2)) / (n_samples_internet)
loss = loss_outdoor + loss_tv + loss_broadcast + loss_internet + \
       λ * (tf.square(W_outdoor) + tf.square(W_outdoor_5) + tf.square(W_tv) +
            tf.square(W_tv_5) + tf.square(W_internet) + tf.square(W_internet_5) +
            tf.square(W_broadcast) + tf.square(W_broadcast_5) + tf.square(W_quality_1) +
            tf.square(W_quality_2) + tf.square(W_time_1) + tf.square(W_time_2) +
            tf.square(W_exposure_1) + tf.square(W_exposure_2))

# 定义优化器，用于更新模型参数 ——选择梯度下降
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss=loss)

# 初始化变量
init = tf.global_variables_initializer()

# 每个display_step得到的损失函数
loss_list = []
# 每个display_step对应的权重
weight_list = []
# 每个display_step对应的截距
bias_list = []

# 开始训练
with tf.Session() as sess:
    # 初始化
    sess.run(init)
    # 迭代训练
    for epoch in range(training_epochs):
        loss_sum = 0.0
        for (x, y) in zip(train_X_outdoor, train_Y_outdoor):
            loss_new, _ = sess.run([loss, optimizer], feed_dict={X_outdoor: x[0], Y_outdoor: y,
                                                                 X_tv: 0.0, Y_tv: 0.0,
                                                                 X_broadcast: 0.0, Y_broadcast: 0.0,
                                                                 X_internet: 0.0, Y_internet: 0.0,
                                                                 X_exposure: x[1],
                                                                 X_quality: x[2],
                                                                 X_time: x[3]
                                                                 })
            loss_sum += loss_new

        for (x, y) in zip(train_X_tv, train_Y_tv):
            loss_new, _ = sess.run([loss, optimizer], feed_dict={X_outdoor: 0.0, Y_outdoor: 0.0,
                                                                 X_tv: x[0], Y_tv: y,
                                                                 X_broadcast: 0.0, Y_broadcast: 0.0,
                                                                 X_internet: 0.0, Y_internet: 0.0,
                                                                 X_exposure: x[1],
                                                                 X_quality: x[2],
                                                                 X_time: x[3]
                                                                 })
            loss_sum += loss_new
        for (x, y) in zip(train_X_broadcast, train_Y_broadcast):
            loss_new, _ = sess.run([loss, optimizer], feed_dict={X_outdoor: 0.0, Y_outdoor: 0.0,
                                                                 X_tv: 0.0, Y_tv: 0.0,
                                                                 X_broadcast: x[0], Y_broadcast: y,
                                                                 X_internet: 0.0, Y_internet: 0.0,
                                                                 X_exposure: x[1],
                                                                 X_quality: x[2],
                                                                 X_time: x[3]
                                                                 })
            loss_sum += loss_new
        for (x, y) in zip(train_X_internet, train_Y_internet):
            loss_new, _ = sess.run([loss, optimizer], feed_dict={X_outdoor: 0.0, Y_outdoor: 0.0,
                                                                 X_tv: 0.0, Y_tv: 0.0,
                                                                 X_broadcast: 0.0, Y_broadcast: 0.0,
                                                                 X_internet: x[0], Y_internet: y,
                                                                 X_exposure: x[1],
                                                                 X_quality: x[2],
                                                                 X_time: x[3]
                                                                 })
            loss_sum += loss_new
        # 展示每次迭代的情况
        if (epoch + 1) % display_step == 0:
            outdoor_weight = round(sess.run(W_outdoor), 5)
            outdoor_bias = round(sess.run(b_outdoor), 5)
            tv_weight = round(sess.run(W_tv), 5)
            tv_bias = round(sess.run(b_tv), 5)
            broadcast_weight = round(sess.run(W_broadcast), 5)
            broadcast_bias = round(sess.run(b_broadcast), 5)
            internet_weight = round(sess.run(W_internet), 5)
            internet_bias = round(sess.run(b_internet), 5)

            print("Epoch : ", "%04d" % (epoch + 1), "Training loss = ", loss_sum,
                  "outdoor_W= ", outdoor_weight, "outdoor_b = ", outdoor_bias,
                  "tv_W= ", tv_weight, "tv_b = ", tv_bias,
                  "broadcast_W= ", broadcast_weight, "broadcast_b = ", broadcast_bias,
                  "internet_W= ", internet_weight, "internet_b = ", internet_bias)

    print("Optimization Finished!")

    print("Training loss = ", loss_sum, "\n")

    # 测试
    test_X_outdoor = np.asarray(
        [[22.6, 40, 2.04, 0.31], [22, 43, 2.13, 0.3], [18.5, 40, 1.63, 0.29], [4.2, 20, 2.11, 0.33],
         [34.4, 56, 2.57, 0.35], [10.8, 31, 1.19, 0.25]])
    test_Y_outdoor = np.asarray([42.8, 41.8, 35.4, 8, 64.7, 20.5])

    test_X_tv = np.asarray([[24, 54, 4.33, 0.35], [6, 27, 3.46, 0.32], [8, 35, 1.69, 0.22], [7.5, 30, 3.52, 0.35]])
    test_Y_tv = np.asarray([26, 6.6, 8.6, 8.1])

    test_X_broadcast = np.asarray([[14.9, 46, 2.69, 0.31], [1, 10, 1.87, 0.29], [8.6, 10, 3.5, 0.3]])
    test_Y_broadcast = np.asarray([16.1, 1, 9.2])

    test_X_internet = np.asarray([[52.8, 66, 7.43, 0.31],
                                  [51.7, 72, 6.63, 0.29]])
    test_Y_internet = np.asarray([105.9, 134])

    print("Testing ... (Mean square loss Comparison)")

    test_loss_outdoor = tf.reduce_sum(tf.pow(pred_outdoor + pred_other_sum - Y_outdoor, 2)) / (test_Y_outdoor.shape[0])
    test_loss_tv = tf.reduce_sum(tf.pow(pred_tv + pred_other_sum - X_tv, 2)) / (test_Y_tv.shape[0])
    test_loss_broadcast = tf.reduce_sum(tf.pow(pred_broadcast + pred_other_sum - Y_broadcast, 2)) / (
        test_Y_broadcast.shape[0])
    test_loss_internet = tf.reduce_sum(tf.pow(pred_internet + pred_other_sum - Y_internet, 2)) / (
        test_Y_internet.shape[0])
    final_testing_loss = test_loss_outdoor + test_loss_tv + test_loss_broadcast + test_loss_internet + \
                         λ * (tf.square(W_outdoor) + tf.square(W_outdoor_5) + tf.square(W_tv) +
                              tf.square(W_tv_5) + tf.square(W_internet) + tf.square(W_internet_5) +
                              tf.square(W_broadcast) + tf.square(W_broadcast_5) + tf.square(W_quality_1) +
                              tf.square(W_quality_2) + tf.square(W_time_1) + tf.square(W_time_2) +
                              tf.square(W_exposure_1) + tf.square(W_exposure_2))
    test_loss_sum = 0
    for (x, y) in zip(test_X_outdoor, test_Y_outdoor):
        loss_new, _ = sess.run([final_testing_loss, optimizer], feed_dict={X_outdoor: x[0], Y_outdoor: y,
                                                                           X_tv: 0.0, Y_tv: 0.0,
                                                                           X_broadcast: 0.0, Y_broadcast: 0.0,
                                                                           X_internet: 0.0, Y_internet: 0.0,
                                                                           X_exposure: x[1],
                                                                           X_quality: x[2],
                                                                           X_time: x[3]
                                                                           })
        test_loss_sum += loss_new

    for (x, y) in zip(test_X_tv, test_Y_tv):
        loss_new, _ = sess.run([final_testing_loss, optimizer], feed_dict={X_outdoor: 0.0, Y_outdoor: 0.0,
                                                                           X_tv: x[0], Y_tv: y,
                                                                           X_broadcast: 0.0, Y_broadcast: 0.0,
                                                                           X_internet: 0.0, Y_internet: 0.0,
                                                                           X_exposure: x[1],
                                                                           X_quality: x[2],
                                                                           X_time: x[3]
                                                                           })
        test_loss_sum += loss_new
    for (x, y) in zip(test_X_broadcast, test_Y_broadcast):
        loss_new, _ = sess.run([final_testing_loss, optimizer], feed_dict={X_outdoor: 0.0, Y_outdoor: 0.0,
                                                                           X_tv: 0.0, Y_tv: 0.0,
                                                                           X_broadcast: x[0], Y_broadcast: y,
                                                                           X_internet: 0.0, Y_internet: 0.0,
                                                                           X_exposure: x[1],
                                                                           X_quality: x[2],
                                                                           X_time: x[3]
                                                                           })
        test_loss_sum += loss_new
    for (x, y) in zip(test_X_internet, test_Y_internet):
        loss_new, _ = sess.run([final_testing_loss, optimizer], feed_dict={X_outdoor: 0.0, Y_outdoor: 0.0,
                                                                           X_tv: 0.0, Y_tv: 0.0,
                                                                           X_broadcast: 0.0, Y_broadcast: 0.0,
                                                                           X_internet: x[0], Y_internet: y,
                                                                           X_exposure: x[1],
                                                                           X_quality: x[2],
                                                                           X_time: x[3]
                                                                           })
        test_loss_sum += loss_new

    print("Testing loss  = ", test_loss_sum)
    print("Absolute mean square loss difference : ", abs(loss_sum - test_loss_sum))

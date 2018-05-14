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
learning_rate = 0.000001
training_epochs = 10000
display_step = 100

# 分类数据
train_X_outdoor = np.asarray(
    [38.4, 36.6, 35.3, 33.8, 24.2, 12.9, 1, 2.5, 2.4, 16.1, 11.4, 33.3, 13.2, 6.0, 4.2, 9.1, 13.9, 33, 32.8, 17.6, 9.7,
     7.4, 12.7, 7.8, 24, 27.6, 20.7, 17.6, 31.6, 30.5, 30.4, 24.2, 25.0])
train_Y_outdoor = np.asarray(
    [69.4, 66.9, 65.9, 64, 45.7, 24.3, 1.5, 4.7, 4.7, 30.5, 21.3, 63.3, 24.7, 11.3, 7.9, 17.3, 26.5, 62.4, 61.9, 32.7,
     18.1, 14.1, 24.1, 14.6, 44.8, 53, 39.3, 33.5, 59.4, 56.7, 57.9, 45.9, 47.1])

train_X_tv = np.asarray([16.9, 1.5, 2.5, 22.2, 25.1, 13.9, 4.5, 12.9, 20.0, 17.9, 10.4, 14.4, 15.7, 10.6, 20.3, 1.6])
train_Y_tv = np.asarray([18.5, 1.6, 2.7, 24.5, 27.2, 15.1, 4.9, 14.0, 21.7, 19.3, 11.3, 15.7, 17.2, 11.5, 21.9, 1.8])

train_X_broadcast = np.asarray([13.6, 23.1, 4.3, 14, 20.8, 12.8, 18.6])
train_Y_broadcast = np.asarray([15, 24.8, 4.6, 15.1, 22.6, 13.7, 20])

train_X_internet = np.asarray([61.9, 50.0, 60.6, 54.8])
train_Y_internet = np.asarray([164.6, 125.3, 159.1, 136.2])

# 获取样本个数
n_samples_outdoor = train_X_outdoor.shape[0]
n_samples_tv = train_X_tv.shape[0]
n_samples_broadcast = train_X_broadcast.shape[0]
n_samples_internet = train_X_internet.shape[0]

# 定义模型的输入和输出
X_outdoor = tf.placeholder("float")
Y_outdoor = tf.placeholder("float")
X_tv = tf.placeholder("float")
Y_tv = tf.placeholder("float")
X_broadcast = tf.placeholder("float")
Y_broadcast = tf.placeholder("float")
X_internet = tf.placeholder("float")
Y_internet = tf.placeholder("float")

# 设置模型的参数
W_outdoor = tf.Variable(rng.randn(), name="weight_outdoor")
b_outdoor = tf.Variable(rng.randn(), name="bias_outdoor")

W_tv = tf.Variable(rng.randn(), name="weight_tv")
b_tv = tf.Variable(rng.randn(), name="bias_tv")

W_broadcast = tf.Variable(rng.randn(), name="weight_broadcast")
b_broadcast = tf.Variable(rng.randn(), name="bias_broadcast")

W_internet = tf.Variable(rng.randn(), name="weight_internet")
b_internet = tf.Variable(rng.randn(), name="bias_internet")

# 构造线性模型
pred_outdoor = tf.add(tf.multiply(X_outdoor, W_outdoor), b_outdoor)
pred_tv = tf.add(tf.multiply(X_tv, W_tv), b_tv)
pred_broadcast = tf.add(tf.multiply(X_broadcast, W_broadcast), b_broadcast)
pred_internet = tf.add(tf.multiply(X_internet, W_internet), b_internet)

# 定义损失函数——均方误差（MSE——mean squared error）

loss_outdoor = tf.reduce_sum(tf.pow(pred_outdoor - Y_outdoor, 2)) / (n_samples_outdoor)
loss_tv = tf.reduce_sum(tf.pow(pred_tv - Y_tv, 2)) / (n_samples_tv)
loss_broadcast = tf.reduce_sum(tf.pow(pred_broadcast - Y_broadcast, 2)) / (n_samples_broadcast)
loss_internet = tf.reduce_sum(tf.pow(pred_internet - Y_internet, 2)) / (n_samples_internet)
loss = loss_outdoor + loss_tv + loss_broadcast + loss_internet

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
        for (x, y) in zip(train_X_outdoor, train_Y_outdoor):
            sess.run(optimizer, feed_dict={X_outdoor: x, Y_outdoor: y,
                                           X_tv: 0.0, Y_tv: 0.0,
                                           X_broadcast: 0.0, Y_broadcast: 0.0,
                                           X_internet: 0.0, Y_internet: 0.0})
        for (x, y) in zip(train_X_tv, train_Y_tv):
            sess.run(optimizer, feed_dict={X_outdoor: 0.0, Y_outdoor: 0.0,
                                           X_tv: x, Y_tv: y,
                                           X_broadcast: 0.0, Y_broadcast: 0.0,
                                           X_internet: 0.0, Y_internet: 0.0})
        for (x, y) in zip(train_X_broadcast, train_Y_broadcast):
            sess.run(optimizer, feed_dict={X_outdoor: 0.0, Y_outdoor: 0.0,
                                           X_tv: 0.0, Y_tv: 0.0,
                                           X_broadcast: x, Y_broadcast: y,
                                           X_internet: 0.0, Y_internet: 0.0})
        for (x, y) in zip(train_X_internet, train_Y_internet):
            sess.run(optimizer, feed_dict={X_outdoor: 0.0, Y_outdoor: 0.0,
                                           X_tv: 0.0, Y_tv: 0.0,
                                           X_broadcast: 0.0, Y_broadcast: 0.0,
                                           X_internet: x, Y_internet: y})

        # 展示每次迭代的情况
        if (epoch + 1) % display_step == 0:
            c = sess.run(loss, feed_dict={X_internet: train_X_internet, Y_internet: train_Y_internet,
                                          X_broadcast: train_X_broadcast, Y_broadcast: train_Y_broadcast,
                                          X_tv: train_X_tv, Y_tv: train_Y_tv,
                                          X_outdoor: train_X_outdoor, Y_outdoor: train_Y_outdoor})
            outdoor_weight = round(sess.run(W_outdoor), 5)
            outdoor_bias = round(sess.run(b_outdoor), 5)
            tv_weight = round(sess.run(W_tv), 5)
            tv_bias = round(sess.run(b_tv), 5)
            broadcast_weight = round(sess.run(W_broadcast), 5)
            broadcast_bias = round(sess.run(b_broadcast), 5)
            internet_weight = round(sess.run(W_internet), 5)
            internet_bias = round(sess.run(b_internet), 5)

            print("Epoch : ", "%04d" % (epoch + 1), "loss = ", "{:.9f}".format(c),
                  "outdoor_W= ", outdoor_weight, "outdoor_b = ", outdoor_bias,
                  "tv_W= ", tv_weight, "tv_b = ", tv_bias,
                  "broadcast_W= ", broadcast_weight, "broadcast_b = ", broadcast_bias,
                  "internet_W= ", internet_weight, "internet_b = ", internet_bias)

    print("Optimization Finished!")
    training_loss = sess.run(loss, feed_dict={X_internet: train_X_internet, Y_internet: train_Y_internet,
                                              X_broadcast: train_X_broadcast, Y_broadcast: train_Y_broadcast,
                                              X_tv: train_X_tv, Y_tv: train_Y_tv,
                                              X_outdoor: train_X_outdoor, Y_outdoor: train_Y_outdoor})
    final_W_outdoor = sess.run(W_outdoor)
    final_b_outdoor = sess.run(b_outdoor)
    final_W_tv = sess.run(W_tv)
    final_b_tv = sess.run(b_tv)
    final_W_broadcast = sess.run(W_broadcast)
    final_b_broadcast = sess.run(b_broadcast)
    final_W_internet = sess.run(W_internet)
    final_b_internet = sess.run(b_internet)
    print("Training loss = ", training_loss,
          "outdoor_W= ", final_W_outdoor, "outdoor_b = ", final_b_outdoor,
          "tv_W= ", final_W_tv, "tv_b = ", final_b_tv,
          "broadcast_W= ", final_W_broadcast, "broadcast_b = ", final_b_broadcast,
          "internet_W= ", final_W_internet, "internet_b = ", final_b_internet, "\n")

    # 画出拟合后的曲线和原始数据的图像
    plt.plot(train_X_outdoor, train_Y_outdoor, "bo", label="Outdoors")
    plt.plot(train_X_outdoor, final_W_outdoor * train_X_outdoor + final_b_outdoor)
    plt.plot(train_X_tv, train_Y_tv, "ro", label="TV")
    plt.plot(train_X_tv, final_W_tv * train_X_tv + final_b_tv)
    plt.plot(train_X_broadcast, train_Y_broadcast, "yo", label="Broadcast")
    plt.plot(train_X_broadcast, final_W_broadcast * train_X_broadcast + final_b_broadcast)
    plt.plot(train_X_internet, train_Y_internet, "go", label="Internet")
    plt.plot(train_X_internet, final_W_internet * train_X_internet + final_b_internet)
    plt.title("Training Data")
    plt.xlabel("Xcost")
    plt.ylabel("Yclick")
    plt.legend()
    plt.show()

    # 测试
    test_X_outdoor = np.asarray([22.6, 22, 18.5, 4.2, 34.4, 10.8])
    test_Y_outdoor = np.asarray([42.8, 41.8, 35.4, 8, 64.7, 20.5])
    test_X_tv = np.asarray([24, 6, 8, 7.5])
    test_Y_tv = np.asarray([26, 6.6, 8.6, 8.1])
    test_X_broadcast = np.asarray([14.9, 1, 8.6])
    test_Y_broadcast = np.asarray([16.1, 1, 9.2])
    test_X_internet = np.asarray([52.8, 51.7])
    test_Y_internet = np.asarray([105.9, 134])

    print("Testing ... (Mean square loss Comparison)")

    test_loss_outdoor = tf.reduce_sum(tf.pow(pred_outdoor - Y_outdoor, 2)) / (test_X_outdoor.shape[0])
    test_loss_tv = tf.reduce_sum(tf.pow(pred_tv - X_tv, 2)) / (test_X_tv.shape[0])
    test_loss_broadcast = tf.reduce_sum(tf.pow(pred_broadcast - Y_broadcast, 2)) / (test_X_broadcast.shape[0])
    test_loss_internet = tf.reduce_sum(tf.pow(pred_internet - Y_internet, 2)) / (test_X_internet.shape[0])
    final_testing_loss = test_loss_outdoor + test_loss_tv + test_loss_broadcast + test_loss_internet
    testing_loss = sess.run(final_testing_loss, feed_dict={X_internet: test_X_internet, Y_internet: test_Y_internet,
                                                           X_broadcast: test_X_broadcast, Y_broadcast: test_Y_broadcast,
                                                           X_tv: test_X_tv, Y_tv: test_Y_tv,
                                                           X_outdoor: test_X_outdoor, Y_outdoor: test_Y_outdoor})

    print("Testing loss  = ", testing_loss)
    print("Absolute mean square loss difference : ", abs(training_loss - testing_loss))

    # 画出测试数据与拟合曲线之间的图像
    plt.plot(test_X_outdoor, test_Y_outdoor, "bo", label="Outdoors")
    plt.plot(train_X_outdoor, final_W_outdoor * train_X_outdoor + final_b_outdoor)
    plt.plot(test_X_tv, test_Y_tv, "ro", label="TV")
    plt.plot(train_X_tv, final_W_tv * train_X_tv + final_b_tv)
    plt.plot(test_X_broadcast, test_Y_broadcast, "yo", label="Broadcast")
    plt.plot(train_X_broadcast, final_W_broadcast * train_X_broadcast + final_b_broadcast)
    plt.plot(test_X_internet, test_Y_internet, "go", label="Internet")
    plt.plot(train_X_internet, final_W_internet * train_X_internet + final_b_internet)
    plt.title("Testing Data")
    plt.xlabel("Xcost")
    plt.ylabel("Yclick")
    plt.legend()
    plt.show()

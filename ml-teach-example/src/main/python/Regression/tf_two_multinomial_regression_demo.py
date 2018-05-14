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
import numpy
import matplotlib.pyplot as plt

rng = numpy.random

# 参数
learning_rate = 0.0000001
training_epochs = 10000
display_step = 100

# 训练数据
train_X = numpy.asarray([1.0, 4.3, 16.9, 17.9, 20.3, 30.5, 35.3, 38.4, 51.7, 61.9])
train_Y = numpy.asarray([1.0, 4.6, 18.5, 19.3, 21.9, 56.7, 65.9, 69.4, 134.0, 164.6])

# # 画出输入和输出的散点图
# plt.plot(train_X, train_Y, "bo")
# plt.xlabel("Xcost")
# plt.ylabel("Y^click")
# plt.show()

# 获取样本个数
n_samples = train_X.shape[0]

# 定义模型的输入和输出
X = tf.placeholder("float")
Y = tf.placeholder("float")

# 设置模型的参数
W_1 = tf.Variable(rng.randn(), name="weight_1")
W_2 = tf.Variable(rng.randn(), name="weight_2")
b = tf.Variable(rng.randn(), name="bias")

# 构造线性模型——增加x*x项
pred = tf.add(tf.multiply(X, W_1), b)
pred = tf.add(pred, tf.multiply(tf.square(X), W_2))

# 定义损失函数——均方误差（MSE——mean squared error）
loss = tf.reduce_sum(tf.pow(pred - Y, 2)) / (n_samples)

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
        for (x, y) in zip(train_X, train_Y):
            sess.run(optimizer, feed_dict={X: x, Y: y})

        # 展示每次迭代的情况
        if (epoch + 1) % display_step == 0:
            c = sess.run(loss, feed_dict={X: train_X, Y: train_Y})
            weight_1 = round(sess.run(W_1), 5)
            weight_2 = round(sess.run(W_2), 5)
            bias = round(sess.run(b), 5)
            loss_list.append(round(c, 5))
            # weight_list.append(weight_1)
            bias_list.append(bias)
            print("Epoch : ", "%04d" % (epoch + 1), "loss = ", "{:.9f}".format(c),
                  "W_1 = ", weight_1, "W_2 = ", weight_2, " b = ", bias)

    print("Optimization Finished!")
    w_1, w_2, b_ = sess.run([W_1, W_2, b])
    training_loss = sess.run(loss, feed_dict={X: train_X, Y: train_Y})
    print("Training loss = ", training_loss, "W_1 = ", w_1, "W_2 = ", w_2, "b = ", b_,
          "\n")

    # 绘制损失函数的值随着训练的次数变化
    plt.plot(range(len(loss_list)), loss_list)
    plt.xlabel("training epoch")
    plt.ylabel("loss")
    plt.title("loss history")
    plt.legend()
    plt.show()

    # 画出拟合后的曲线和原始数据的图像
    plt.plot(train_X, train_Y, "ro", label="Original data")
    plt.plot(train_X, w_2 * numpy.power(train_X, 2) + w_1 * train_X + b_, label="Fitted line")
    plt.title("Training Data")
    plt.xlabel("Xcost")
    plt.ylabel("Yclick")
    plt.legend()
    plt.show()

    # 测试

    test_X = numpy.asarray([33.8, 24.2, 10.4, 14.4, 12.8, 8.6, 50.0, 60.6])
    test_Y = numpy.asarray([64.0, 45.7, 11.3, 15.7, 13.7, 9.2, 125.3, 159.1])

    print("Testing ... (Mean square loss Comparison)")
    testing_loss = sess.run(tf.reduce_sum(tf.pow(pred - Y, 2)) / (test_X.shape[0]),
                            feed_dict={X: test_X, Y: test_Y})
    print("Testing loss  = ", testing_loss)
    print("Absolute mean square loss difference : ", abs(training_loss - testing_loss))

    # 画出测试数据与拟合曲线之间的图像
    plt.plot(test_X, test_Y, "bo", label="Testing data")
    plt.plot(train_X, w_2 * numpy.power(train_X, 2) + w_1 * train_X + b_, label="Fitted line")
    plt.xlabel("Xcost")
    plt.ylabel("Yclick")
    plt.legend()
    plt.show()

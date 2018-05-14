#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/5/7 0007'
__author__ = 'Administrator'
__filename__ = 'train_test_error_plot'
"""

import numpy as np
import matplotlib.pyplot as plt

# # 画出输入和输出的散点图
# train_error = np.asarray([292.20038, 23.525003, 23.383276, 22.241686, 21.8645])
# x_num = np.asarray([1, 2, 3, 4, 5])
# test_error = np.asarray([205.39616, 32.219296, 44.037914, 45.970238, 48.466515])
#
# plt.plot(x_num, train_error, "bo-", label="Training Error")
# plt.plot(x_num, test_error, "ko-", label="Testing Error")
# plt.title("Training Error Vs. Testing Error")
# plt.xlabel("Polynomial number")
# plt.ylabel("MSE")
# #增加才会展示label
# plt.legend()
# plt.show()

#正则化对比
train_error = np.asarray([21.9,22.3,23.5,24.1,25.6,26.3,28.5])
x_num = np.asarray([0,1,10,100,1000,10000,100000])
test_error = np.asarray([102.3,68.7,35.7,21.1,22.8,28.7,36.8])

plt.plot(x_num, train_error, "bo-", label="Training")
plt.plot(x_num, test_error, "ko-", label="Testing")
plt.xlabel("λ")
plt.ylabel("MSE")
#增加才会展示label
plt.legend()
plt.show()

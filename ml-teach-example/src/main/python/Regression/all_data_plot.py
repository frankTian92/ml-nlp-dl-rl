#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/5/8 0008'
__author__ = 'Administrator'
__filename__ = 'all_data_plot'
"""
import numpy as np
import matplotlib.pyplot as plt
# 全量数据
# train_X = np.asarray([38.4,36.6,35.3,33.8,24.2,12.9,1,2.5,2.4,16.1,11.4,33.3,13.2,6,4.2,9.1,13.9,33,32.8,17.6,9.7,7.4,12.7,7.8,24,27.6,20.7,17.6,31.6,30.5,30.4,24.2,25,22.6,22,18.5,4.2,34.4,10.8,16.9,1.5,2.5,22.2,25.1,13.9,4.5,12.9,20,17.9,10.4,14.4,15.7,10.6,20.3,1.6,24,6,8,7.5,13.6,23.1,4.3,14,20.8,12.8,18.6,14.9,1,8.6,61.9,50,60.6,54.8,52.8,51.7])
# train_Y = np.asarray([69.4,66.9,65.9,64,45.7,24.3,1.5,4.7,4.7,30.5,21.3,63.3,24.7,11.3,7.9,17.3,26.5,62.4,61.9,32.7,18.1,14.1,24.1,14.6,44.8,53,39.3,33.5,59.4,56.7,57.9,45.9,47.1,42.8,41.8,35.4,8,64.7,20.5,18.5,1.6,2.7,24.5,27.2,15.1,4.9,14,21.7,19.3,11.3,15.7,17.2,11.5,21.9,1.8,26,6.6,8.6,8.1,15,24.8,4.6,15.1,22.6,13.7,20,16.1,1,9.2,164.6,125.3,159.1,136.2,105.9,134.0])
# plt.plot(train_X,train_Y,"bo")
# plt.xlabel("Xcost")
# plt.ylabel("Yclick")
# plt.show()

# # 分类数据
# train_X_outdoor = np.asarray([38.4,36.6,35.3,33.8,24.2,12.9,1,2.5,2.4,16.1,11.4,33.3,13.2,6,4.2,9.1,13.9,33,32.8,17.6,9.7,7.4,12.7,7.8,24,27.6,20.7,17.6,31.6,30.5,30.4,24.2,25,22.6,22,18.5,4.2,34.4,10.8])
# train_Y_outdoor = np.asarray([69.4,66.9,65.9,64,45.7,24.3,1.5,4.7,4.7,30.5,21.3,63.3,24.7,11.3,7.9,17.3,26.5,62.4,61.9,32.7,18.1,14.1,24.1,14.6,44.8,53,39.3,33.5,59.4,56.7,57.9,45.9,47.1,42.8,41.8,35.4,8,64.7,20.5])
#
# train_X_tv = np.asarray([16.9,1.5,2.5,22.2,25.1,13.9,4.5,12.9,20,17.9,10.4,14.4,15.7,10.6,20.3,1.6,24,6,8,7.5])
# train_Y_tv = np.asarray([18.5,1.6,2.7,24.5,27.2,15.1,4.9,14,21.7,19.3,11.3,15.7,17.2,11.5,21.9,1.8,26,6.6,8.6,8.1])
#
# train_X_broadcast = np.asarray([13.6,23.1,4.3,14,20.8,12.8,18.6,14.9,1,8.6])
# train_Y_broadcast = np.asarray([15,24.8,4.6,15.1,22.6,13.7,20,16.1,1,9.2])
#
# train_X_internet = np.asarray([61.9,50,60.6,54.8,52.8,51.7])
# train_Y_internet = np.asarray([164.6,125.3,159.1,136.2,105.9,134])
#
# plt.plot(train_X_outdoor,train_Y_outdoor,"bo",label="Outdoors")
# plt.plot(train_X_tv,train_Y_tv,"ro",label = "TV")
# plt.plot(train_X_broadcast,train_Y_broadcast,"yo",label="Broadcast")
# plt.plot(train_X_internet,train_Y_internet,"go",label = "Internet")
# plt.xlabel("Xcost")
# plt.ylabel("Yclick")
# plt.title("Types of Advertisement")
# plt.legend()
# plt.show()


#其他因素图像
train_y = np.asarray([38.4,36.6,35.3,33.8,24.2,12.9,1,2.5,2.4,16.1,11.4,33.3,13.2,6,4.2,9.1,13.9,33,32.8,17.6,9.7,7.4,12.7,7.8,24,27.6,20.7,17.6,31.6,30.5,30.4,24.2,25,22.6,22,18.5,4.2,34.4,10.8,16.9,1.5,2.5,22.2,25.1,13.9,4.5,12.9,20,17.9,10.4,14.4,15.7,10.6,20.3,1.6,24,6,8,7.5,13.6,23.1,4.3,14,20.8,12.8,18.6,14.9,1,8.6,61.9,50,60.6,54.8,52.8,51.7])
#曝光度
train_x_exposure = np.asarray([56,54,55,51,45,35,10,14,13,35,31,52,33,21,19,29,34,48,48,35,30,24,32,26,41,48,41,35,47,53,46,43,42,40,43,40,20,56,31,45,15,17,48,56,46,27,45,49,47,36,48,49,39,52,13,54,27,35,30,44,62,26,49,53,46,56,46,10,10,74,64,74,66,66,72])
plt.plot(train_x_exposure,train_y,"bo")
plt.xlabel("X_exposure")
plt.ylabel("Y_click")
plt.show()

#quality广告质量
train_x_quality = np.asarray([2.31,1.67,1.94,1.73,1.44,2.07,0.92,2.72,2.07,1.45,1.58,1.85,1.63,1.67,2.01,2.68,1.76,1.62,1.62,1.81,1.95,0.78,2.33,2.11,2.53,0.87,1.19,1.68,1.71,2.04,1.99,2.09,0.95,2.04,2.13,1.63,2.11,2.57,1.19,3.38,3.27,3.11,2.93,4.51,4.5,2.55,4.01,2.62,3.95,3.48,2.6,2.05,5.31,3.54,2.68,4.33,3.46,1.69,3.52,4.68,3.8,2.68,2.7,2.24,1.69,3.14,2.69,1.87,3.5,2.87,5.11,10.42,6.87,7.43,6.63])
plt.plot(train_x_quality,train_y,"bo")
plt.xlabel("X_quality")
plt.ylabel("Y_click")
plt.show()

#time广告时长
train_x_time = np.asarray([0.34,0.29,0.3,0.31,0.27,0.35,0.25,0.37,0.32,0.31,0.26,0.3,0.28,0.3,0.3,0.35,0.31,0.29,0.3,0.29,0.31,0.26,0.34,0.32,0.33,0.24,0.26,0.31,0.27,0.32,0.31,0.34,0.26,0.31,0.3,0.29,0.33,0.35,0.25,0.29,0.28,0.29,0.29,0.34,0.32,0.29,0.34,0.27,0.35,0.31,0.29,0.28,0.39,0.3,0.26,0.35,0.32,0.22,0.35,0.35,0.32,0.28,0.3,0.29,0.24,0.27,0.31,0.29,0.3,0.2,0.26,0.38,0.32,0.31,0.29])
plt.plot(train_x_time,train_y,"bo")
plt.xlabel("X_time")
plt.ylabel("Y_click")
plt.show()
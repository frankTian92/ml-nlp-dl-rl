#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/5/21 0021'
__author__ = 'Administrator'
__filename__ = 'test'
"""


import numpy as np

def get_batches(arr, n_seqs, n_steps):
    '''
    对已有的数组进行mini_batch分割
    :param arr: 待分割的数组
    :param n_seqs: 一个batch中的序列个数
    :param n_steps:单个序列长度
    :return:
    '''
    batch_size = n_seqs * n_steps
    n_batches = int(len(arr) / batch_size)
    # 这个地方我们仅保留完成的batch(full batch),也就是说对于不能整除的部分进行舍弃
    arr = arr[:batch_size * n_batches]

    # 重塑
    arr = arr.reshape((n_seqs, -1))

    for n in range(0, arr.shape[1], n_steps):
        x = arr[:, n:n + n_steps]
        # 注意targets相比于x会向后错一个字符
        y = np.zeros_like(x)
        y[:, :-1], y[:, -1] = x[:, 1:], x[:, 0]
        yield x, y


with open('D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\demo_data\\anna.txt', 'r') as f:
    text = f.read()
vocab = set(text)
vocab_to_int = {c: i for i, c in enumerate(vocab)}
int_to_vocab = dict(enumerate(vocab))
encode = np.array([vocab_to_int[c] for c in text], dtype=np.int32)
x,y = next(get_batches(encode,10,50))
print('x\n', x[:10, :10])
print('\ny\n', y[:10, :10])



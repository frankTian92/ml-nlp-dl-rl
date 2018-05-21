#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/5/18 0018'
__author__ = 'Administrator'
__filename__ = 'LSTMDemo'
"""
import time
import numpy as np
import tensorflow as tf

# 构建训练数据集
# text = ["a", "b", "c", "d", "e"]
# vocab = set(text)
# vocab_to_int = {c: i for i, c in enumerate(vocab)}
# int_to_vocab = dict(enumerate(vocab))
# encode = np.array([vocab_to_int[c] for c in text], dtype=np.int32)

with open('D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\demo_data\\anna.txt', 'r') as f:
    text = f.read()
vocab = set(text)
vocab_to_int = {c: i for i, c in enumerate(vocab)}
int_to_vocab = dict(enumerate(vocab))
encode = np.array([vocab_to_int[c] for c in text], dtype=np.int32)


# mini-batch的分割:
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


# 输入层
def build_inputs(num_seqs, num_steps):
    '''
    构建输入层
    :param num_seqs:每个batch 的序列个数
    :param num_steps: 每个序列包含的字符数
    :return:
    '''
    inputs = tf.placeholder(tf.int32, shape=(num_seqs, num_steps), name="inputs")
    targets = tf.placeholder(tf.int32, shape=(num_seqs, num_steps), name="targets")

    # 加入keep_prob
    keep_prob = tf.placeholder(tf.float32, name="keep_prob")
    return inputs, targets, keep_prob


# LSTM层
def build_lstm(lstm_size, num_layers, batch_size, keep_prob):
    '''
    构建LSTMc层
    :param lstm_size: 隐含层大小
    :param num_layers: 网络深度
    :param batch_size:
    :param keep_prob:
    :return:
    '''
    lstm = tf.nn.rnn_cell.BasicLSTMCell(lstm_size)
    drop = tf.nn.rnn_cell.DropoutWrapper(lstm, output_keep_prob=keep_prob)

    # 堆叠多个LSTM单位
    cell = tf.nn.rnn_cell.MultiRNNCell([drop for _ in range(num_layers)])
    initial_state = cell.zero_state(batch_size, tf.float32)
    return cell, initial_state


# 输出层
def build_output(lstm_output, in_size, out_size):
    '''
    构建输出层
    :param lstm_output: LSTM输出的结果（是一个三维数组）
    :param in_size: LSTM层重塑后的size
    :param out_size: softmax层的size
    :return:
    '''
    # 将LSTM的输出按照列concate,例如[[1,2,3],[7,8,9]]
    # tf.concate的输出结果是[1,2,3,7,8,9]
    seq_output = tf.concat(lstm_output, axis=1)
    # reshape
    x = tf.reshape(seq_output, [-1, in_size])

    # 将lstm层与softmax层全连接
    with tf.variable_scope("softmax"):
        softmax_w = tf.Variable(tf.truncated_normal([in_size, out_size], stddev=0.1))
        softmax_b = tf.Variable(tf.zeros(out_size))

    # 计算logits
    logits = tf.matmul(x, softmax_w) + softmax_b

    # 计算softmax层返回概率分布
    out = tf.nn.softmax(logits, name="predictions")
    return out, logits


# 训练误差计算
def build_loss(logits, targets, lstm_size, num_classes):
    '''
    根据logits和targets计算损失
    :param logits: 全连接层输出的结果，没有经过softmax
    :param tragets: 目标字符
    :param lstm_size: LSTM cell隐层节点的数量
    :param num_classes: 词表大小
    :return:
    '''
    # 对targets进行编码
    y_one_hot = tf.one_hot(targets, num_classes)
    y_reshaped = tf.reshape(y_one_hot, logits.get_shape())

    # softmax cross entropy between logits and labels
    loss = tf.nn.softmax_cross_entropy_with_logits(logits, labels=y_reshaped)
    loss = tf.reduce_mean(loss)
    return loss


# 优化器
def build_optimizer(loss, learning_rate, grad_clip):
    '''
    构造优化器
    :param loss: 损失
    :param learning_rate: 学习率
    :param grad_clip:
    :return:
    '''
    # 使用处理clipping gradients
    tvars = tf.trainable_variables()
    grads, _ = tf.clip_by_global_norm(tf.gradients(loss, tvars), grad_clip)
    train_op = tf.train.AdamOptimizer(learning_rate=learning_rate)
    optimizer = train_op.apply_gradients(zip(grads, tvars))
    return optimizer


# 模型组合
class CharRNN:
    def __init__(self, num_classes, batch_size=64, num_steps=50, lstm_size=128,
                 num_layers=2, learning_rate=0.001, grap_clip=5, sampling=False):
        # 如果sample是True，则采用SGD
        if sampling == True:
            batch_size, num_steps = 1, 1
        else:
            batch_size, num_steps = batch_size, num_steps
        tf.reset_default_graph()

        # 输入层
        self.inputs, self.targets, self.keep_prob = build_inputs(batch_size, num_steps)

        # LSTM层
        cell, self.initial_state = build_lstm(lstm_size, num_layers, batch_size, self.keep_prob)

        # 对输入进行one-hot编码
        x_one_hot = tf.one_hot(self.inputs, num_classes)

        # 运行RNN
        outputs, state = tf.nn.dynamic_rnn(cell, x_one_hot, initial_state=self.initial_state)
        self.final_state = state

        # 预测结果
        self.prediction, self.logits = build_output(outputs, lstm_size, num_classes)

        # loss和optimizer(with gradient clipping)
        self.loss = build_loss(self.logits, self.targets, lstm_size, num_classes)
        self.optimizer = build_optimizer(self.loss, learning_rate, grap_clip)


# # 模型训练
# def trainModel():
# 单个batch中序列的个数
batch_size = 100
# 单个序列中字符数目
num_seteps = 100
# 隐含节点个数
lstm_size = 512
# LSTM层的个数
num_layers = 2
# 学习率
learning_rate = 0.001
# 训练中dropout层直接拍保留的结点比例
keep_prob = 0.5

# 迭代次数
epoches = 20
# 每n轮进行一次变量保存
save_every_n = 200
model = CharRNN(len(vocab), batch_size=batch_size, num_steps=num_seteps,
                    lstm_size=lstm_size, num_layers=num_layers,
                    learning_rate=learning_rate)
saver = tf.train.Saver(max_to_keep=100)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    counter = 0
    for e in range(epoches):
        # 训练模型
        new_state = sess.run(model.initial_state)
        loss = 0
        for x, y in get_batches(encode, batch_size, num_seteps):
            counter += 1
            start = time.time()
            feed = {model.inputs: x,
                    model.targets: y,
                    model.keep_prob: keep_prob,
                    model.initial_state: new_state}
            batch_loss, new_state, _ = sess.run(model.loss,
                                                    model.final_state,
                                                    model.optimizer,
                                                    feed_dict=feed)
            end = time.time()
            # 打印详情
            if counter % 500 == 0:
                    print("轮数 ：{}/{}... ".format(e + 1, epoches),
                          "训练步数：{}... ".format(counter),
                          "训练误差： {:.4f}... ".format(batch_loss),
                          "{:.4f} sec/batch".format(end - start))
            if (counter % save_every_n == 0):
                    saver.save(sess, "ckeckpoints/i{}_1{}.ckpt".format(counter, lstm_size))

    saver.save(sess, "ckeckpoints/i{}_1{}.ckpt".format(counter, lstm_size))


# if __name__ == '__main__':
#     trainModel()

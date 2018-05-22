# coding=utf-8
'''
Created on 2017年2月19日

@author: Lu.yipiao
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.contrib as tc
import logging
import time
import os


class StockModel(object):
    """
    Implements the main Stock Predict model.
    """

    def __init__(self, layer_num):
        # logging
        logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # the constant
        self.time_step = 20  # 时间步
        self.hidden_size = 10  # hidden layer units
        self.batch_size = 60  # 每一批次训练多少个样例
        self.input_size = 1  # 输入层维度
        self.output_size = 1  # 输出层维度
        self.lr = 0.0006  # 学习率
        self.keep_prob = 0.9  # drop out 后的比例
        self.layer_num = layer_num  # LSTM层数


        # session info
        sess_config = tf.ConfigProto()
        sess_config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=sess_config)

        self._build_graph()

        # save info
        self.saver = tf.train.Saver(tf.global_variables())

        # initialize the model
        self.sess.run(tf.global_variables_initializer())

    def _build_graph(self):
        """
         Builds the computation graph with Tensorflow
        """
        start_t = time.time()
        self.load_data()
        self.get_train_data()
        self.plot_data()
        self._setup_placeholders()
        self.lstm()
        self._compute_loss()
        self._create_train_op()
        self.logger.info('Time to build graph: {} s'.format(time.time() - start_t))
        param_num = sum([np.prod(self.sess.run(tf.shape(v))) for v in self.all_params])
        self.logger.info('There are {} parameters in the model'.format(param_num))

    def load_data(self):
        f = open('D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\stock_predict\\data\\dataset_1.csv')
        df = pd.read_csv(f)  # 读入股票数据
        data = np.array(df['最高价'])  # 获取最高价序列
        data = data[::-1]  # 反转，使数据按照日期先后顺序排列
        normalize_data = (data - np.mean(data)) / np.std(data)  # 标准化
        normalize_data = normalize_data[:, np.newaxis]  # 增加维度
        self.data = normalize_data
        self.logger.info("数据加载完成")

    def plot_data(self):
        # 以折线图展示data
        plt.figure()
        plt.plot(self.data)
        plt.show()

    # 生成训练集
    def get_train_data(self):
        self.train_x, self.train_y = [], []  # 训练集
        for i in range(len(self.data) - self.time_step - 1):
            x = self.data[i:i + self.time_step]
            y = self.data[i + 1:i + self.time_step + 1]
            self.train_x.append(x.tolist())
            self.train_y.append(y.tolist())

    def _setup_placeholders(self):
        """
        Placeholders
        """
        # 每批次输入网络的tensor
        self.X = tf.placeholder(tf.float32, [None, self.time_step, self.input_size], name="X")
        # 每批次tensor对应的标签
        self.Y = tf.placeholder(tf.float32, [None, self.time_step, self.input_size], name="Y")

        # 输入层、输出层权重、偏置
        self.weights = {
            'in': tf.Variable(tf.random_normal([self.input_size, self.hidden_size]), name="weight_in"),
            'out': tf.Variable(tf.random_normal([self.hidden_size, 1]), name="weight_out")
        }
        self.biases = {
            'in': tf.Variable(tf.constant(0.1, shape=[self.hidden_size, ]), name="biases_in"),
            'out': tf.Variable(tf.constant(0.1, shape=[1, ]), name="biases_out")
        }

    def get_cell(self, hidden_size, layer_num=1, dropout_keep_prob=None):
        """
        Gets the RNN Cell
        """
        cells = []
        for i in range(layer_num):
            cell = tc.rnn.LSTMCell(num_units=hidden_size, state_is_tuple=True)
            if dropout_keep_prob is not None:
                cell = tc.rnn.DropoutWrapper(cell,
                                             input_keep_prob=dropout_keep_prob,
                                             output_keep_prob=dropout_keep_prob)
        cells.append(cell)
        cells = tc.rnn.MultiRNNCell(cells, state_is_tuple=True)
        return cells

    # 定义神经网络
    def lstm(self):  # 参数：输入网络批次数目
        w_in = self.weights['in']
        b_in = self.biases['in']
        input = tf.reshape(self.X, [-1, self.input_size])  # 需要将tensor转成2维进行计算，计算后的结果作为隐藏层的输入
        input_rnn = tf.matmul(input, w_in) + b_in
        input_rnn = tf.reshape(input_rnn, [-1, self.time_step, self.hidden_size])  # 将tensor转成3维，作为lstm cell的输入
        # with tf.variable_scope(scope_name):
        cell = self.get_cell(hidden_size=self.hidden_size, layer_num=self.layer_num, dropout_keep_prob=self.keep_prob)
        init_state = cell.zero_state(batch_size=self.batch_size, dtype=tf.float32)
        # output_rnn是记录lstm每个输出节点的结果，final_states是最后一个cell的结果
        output_rnn, final_states = tf.nn.dynamic_rnn(cell, input_rnn, initial_state=init_state, dtype=tf.float32)
        output = tf.reshape(output_rnn, [-1, self.hidden_size])  # 作为输出层的输入
        w_out = self.weights['out']
        b_out = self.biases['out']
        pred = tf.matmul(output, w_out) + b_out
        self.pred = pred
        self.final_states = final_states

    # 定义损失函数
    def _compute_loss(self):
        self.all_params = tf.trainable_variables()
        self.loss = tf.reduce_mean(tf.square(tf.reshape(self.pred, [-1]) - tf.reshape(self.Y, [-1])))

    # 定义优化器
    def _create_train_op(self):
        self.optimizer = tf.train.AdamOptimizer(self.lr)
        self.train_op = self.optimizer.minimize(self.loss)

    # 模型训练一个epoch
    def _train_epoch(self, train_batch_x, train_batch_y):

        feed_dict = {self.X: train_batch_x,
                     self.Y: train_batch_y
                     }
        _, loss = self.sess.run([self.train_op, self.loss], feed_dict)
        return loss

    # 预测训练一个epoch
    def _predict_epoch(self, predict_epoch_x):
        feed_dict = {self.X: predict_epoch_x}
        predict = self.sess.run(self.pred, feed_dict=feed_dict)
        return predict

    def train_lstm(self,train_nums):
            # 重复训练10000次
            for epoch in range(train_nums):
                start = 0
                end = start + self.batch_size
                while (end < len(self.train_x)):
                    loss = self._train_epoch(self.train_x[start:end], self.train_y[start:end])
                    start += self.batch_size
                    end = start + self.batch_size
                print(epoch, loss)
                self.save('D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\stock_predict\\model_1\\',
                                  "stock.model")


    # 模型预测
    def prediction(self,predict_num):
        # 参数恢复
        module_file = tf.train.latest_checkpoint(
            'D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\stock_predict\\model_1\\')
        self.saver.restore(self.sess, module_file)

        # 取训练集最后一行为测试样本。shape=[1,time_step,input_size]
        prev_seq = self.train_x[-1]
        predict = []
        # 得到之后100个预测结果
        for epoch in range(1000):
            next_seq = self._predict_epoch([prev_seq])
            predict.append(next_seq[-1])
            # 每次得到最后一个时间步的预测结果，与之前的数据加在一起，形成新的测试样本
            prev_seq = np.vstack((prev_seq[1:], next_seq[-1]))
        # 以折线图表示结果
        plt.figure()
        plt.plot(list(range(len(self.data))), self.data, color='b')
        plt.plot(list(range(len(self.data), len(self.data) + len(predict))), predict, color='r')
        plt.show()

        # 模型保存

    def save(self, model_dir, model_prefix):
        self.saver.save(self.sess, os.path.join(model_dir, model_prefix))
        self.logger.info('Model saved in {}, with prefix {}.'.format(model_dir, model_prefix))


if __name__ == '__main__':
    stock_model = StockModel(5)
    stock_model.train_lstm(20)
    stock_model.prediction(20)

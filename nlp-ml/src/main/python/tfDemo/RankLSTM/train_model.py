#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import numpy as np
import tensorflow as tf
import time
from src.main.python.tfDemo.RankLSTM.DataSet import DataSet

# -------------------------------数据预处理---------------------------#

poetry_file = 'D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\demo_data\\rank.txt'

# 排序记录
rank_list = []
with open(poetry_file, "rb") as f:
    for line in f:
        try:
            line = line.decode('UTF-8')
            line = line.strip(u'\n\r')
            rank = line.split(u',')
            if len(rank) < 2:
                continue


            if len(rank) > 2:
                for i in range(len(rank) - 2):
                    rank_sub_1 = rank[(i + 1):]
                    rank_sub_1.append("end")
                    if rank_sub_1 not in rank_list:
                        rank_list.append(rank_sub_1)

                    rank_sub_2 = rank[i:(i + 2)]
                    rank_sub_2.append("end")
                    if rank_sub_2 not in rank_list:
                        rank_list.append(rank_sub_2)

                rank.append("end")
                if rank not in rank_list:
                    rank_list.append(rank)

            else:
                rank.append("end")
                if rank not in rank_list:
                    rank_list.append(rank)

        except Exception as e:
            pass

print('排序总数: ', len(rank_list))

# 构建词典
words = ["a", "b", "c", "d", "e","end"]

# 每个字映射为一个数字ID
word_num_map = dict(zip(words, range(len(words))))
# 把诗转换为向量形式，参考TensorFlow练习1
to_num = lambda word: word_num_map.get(word, len(words))
ranks_vector = [list(map(to_num, ranks)) for ranks in rank_list]


class LSTMDemo(object):
    def __init__(self, vocab,is_training,batch_size):

        # session info
        sess_config = tf.ConfigProto()
        sess_config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=sess_config)

        # basic config
        # the vocab
        self.vocab = vocab
        self.is_training = is_training
        self.rnn_size = 64
        self.num_layers = 6
        self.batch_size = batch_size
        self.keep_prob = 1.0
        self._build_graph()

        # save info
        self.saver = tf.train.Saver()

        # initialize the model
        #
        self.sess.run(tf.global_variables_initializer())

    def _build_graph(self):
        """
        Builds the computation graph with Tensorflow
        """
        start_t = time.time()
        self._setup_placeholders()
        self._embed()
        self._neural_network()
        self._compute_loss()
        self._create_train_op()
        print('Time to build graph: {} s'.format(time.time() - start_t))
        param_num = sum([np.prod(self.sess.run(tf.shape(v))) for v in self.all_params])
        print('There are {} parameters in the model'.format(param_num))

    def _setup_placeholders(self):
        """
        Placeholders
        """
        self.input_data = tf.placeholder(tf.int32, [self.batch_size, None], name="input_data")
        self.output_targets = tf.placeholder(tf.int32, [self.batch_size, None], name="output_targets")
        # self.input_data_seq_length = tf.placeholder(tf.float32, batch_size, name="input_data_seq_length")

    def _embed(self):
        """
        The embedding layer, question and passage share embeddings
        """
        with tf.device('/cpu:0'), tf.variable_scope('word_embedding'):
            self.word_embeddings = tf.get_variable(
                'word_embeddings',
                shape=(len(self.vocab), self.rnn_size),
                trainable=True
            )
            self.input = tf.nn.embedding_lookup(self.word_embeddings, self.input_data)

        if self.is_training and self.keep_prob<1:
            self.input = tf.nn.dropout(self.input,self.keep_prob)

    # 定义RNN
    def _neural_network(self):

        cell_fun = tf.nn.rnn_cell.BasicLSTMCell
        # cell_fun = tf.nn.rnn_cell.GRUCell
        cell = cell_fun(self.rnn_size)
        if self.is_training and self.keep_prob<1:
             cell = tf.nn.rnn_cell.DropoutWrapper(cell, output_keep_prob=self.keep_prob)
        rnn_cells = tf.nn.rnn_cell.MultiRNNCell([cell] * self.num_layers, state_is_tuple=True)

        outputs, last_state = tf.nn.dynamic_rnn(rnn_cells, self.input, dtype=tf.float32, scope='rnnlm')

        with tf.variable_scope('rnnlm'):
            softmax_w = tf.get_variable("softmax_w", [self.rnn_size, len(self.vocab)])
            softmax_b = tf.get_variable("softmax_b", [len(self.vocab)])

        output = tf.reshape(outputs, [-1, self.rnn_size])

        # self.logits = tf.tanh(tf.matmul(output, softmax_w),name="tanh") + softmax_b
        self.logits = tf.matmul(output, softmax_w) + softmax_b
        self.probs = tf.nn.softmax(self.logits)

    # 定义损失函数
    def _compute_loss(self):
        targets = tf.reshape(self.output_targets, [-1])
        # 交叉熵的和
        loss_sum = tf.contrib.legacy_seq2seq.sequence_loss_by_example([self.logits], [targets],
                                                                      [tf.ones_like(targets, dtype=tf.float32)],
                                                                      len(self.vocab))
        self.loss = tf.reduce_mean(loss_sum)
        self.all_params = tf.trainable_variables()

    # 定义优化器
    def _create_train_op(self):
        # 使用剪纸的adam优化器
        self.learning_rate = tf.Variable(0.0, trainable=False)
        tvars = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.loss, tvars), 5)
        optimizer = tf.train.AdamOptimizer(self.learning_rate)
        self.train_op = optimizer.apply_gradients(zip(grads, tvars))

    # 模型加载
    def load_model(self, ckpt_path):
        latest_ckpt = tf.train.latest_checkpoint(ckpt_path)
        if latest_ckpt:
            print('resume from', latest_ckpt)
            self.saver.restore(self.sess, latest_ckpt)
            return int(latest_ckpt[latest_ckpt.rindex('-') + 1:])
        else:
            print('building model from scratch')
            self.sess.run(tf.global_variables_initializer())
            return -1

    # 训练
    def train_neural_network(self,train_datas,epoches,isReTrain):

        ckpt_path = 'D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\model\\protry_model\\'
        if isReTrain:
            latest_ckpt = tf.train.latest_checkpoint(ckpt_path)
            self.saver = tf.train.import_meta_graph(latest_ckpt + ".meta")
            self.saver.restore(self.sess, latest_ckpt)
            last_epoch = int(latest_ckpt[latest_ckpt.rindex('-') + 1:])
        else:
            last_epoch = self.load_model(ckpt_path)

        min_loss = 2.59
        for epoch in range(last_epoch + 1, epoches):
            self.sess.run(tf.assign(self.learning_rate,0.00002))
            all_loss = 10
            train_batch = train_datas.next_batch(self.batch_size)
            for batch_num, batch_data in enumerate(train_batch):
                train_loss, _, lr = self.sess.run([self.loss, self.train_op, self.learning_rate],
                                                  feed_dict={self.input_data: batch_data["xdata"],
                                                             self.output_targets: batch_data["ydata"]
                                                             })
                # if batch_num % 2 == 1:
                #     print(epoch, (batch_num + 1) * batch_size, 0.002 * (0.97 ** epoch), train_loss)

                all_loss = all_loss + train_loss

            if (all_loss * 1.0 / (batch_num + 1) * self.batch_size < min_loss):
                min_loss = all_loss * 1.0 / (batch_num + 1) * self.batch_size
                self.saver.save(self.sess,
                                'D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\model\\protry_model\\poetry.module',
                                global_step=epoch)
            print(epoch, 'lr: ', lr, ' Loss: ', all_loss * 1.0 / (batch_num + 1) * self.batch_size)


    # 预测
    def predict(self, word):

        def to_word(weights):
            results = []
            for weight in weights:
                sample = np.argmax(weight)
                results.append(self.vocab[sample])
            return results

        x = np.array([list(map(word_num_map.get, word))])
        # #预测是时候重新分配模型的batch_size
        # self.sess.run(tf.assign(self.batch_size , x.shape[0]))
        prob = self.sess.run(self.probs, feed_dict={self.input_data: x})
        pred_result = to_word(prob)
        print(pred_result)
        print(list(prob))

    def restore(self, ckpt_path):
        latest_ckpt = tf.train.latest_checkpoint(ckpt_path)
        self.saver = tf.train.import_meta_graph(latest_ckpt + ".meta")
        self.saver.restore(self.sess, latest_ckpt)
        print('Model restored from {}='.format(latest_ckpt))


def predict(words, word,batch_size):
    lstm = LSTMDemo(words,is_training=False,batch_size=batch_size)
    lstm.restore("D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\model\\protry_model\\")
    lstm.predict(word)


if __name__ == '__main__':
    word = ["a"]
    # train_datas = DataSet(data_vector= ranks_vector,word_num_map=word_num_map,filter_length=None)
    # lstm = LSTMDemo(vocab=words,is_training=True,batch_size=1)
    # lstm.train_neural_network(train_datas=train_datas,epoches=10000,isReTrain=False)
    # lstm.predict(word=word)


    predict(words,word,batch_size=1)
    print(words)

# -*- coding:utf8 -*-
# ==============================================================================
# Copyright 2017 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""
This module implements the core layer of Match-LSTM and BiDAF
"""

import tensorflow as tf
import tensorflow.contrib as tc


class MatchLSTMAttnCell(tc.rnn.LSTMCell):
    """
    Implements the Match-LSTM attention cell
    """
    def __init__(self, num_units, context_to_attend):
        super(MatchLSTMAttnCell, self).__init__(num_units, state_is_tuple=True)
        self.context_to_attend = context_to_attend
        self.fc_context = tc.layers.fully_connected(self.context_to_attend,
                                                    num_outputs=self._num_units,
                                                    activation_fn=None)

    def __call__(self, inputs, state, scope=None):
        (c_prev, h_prev) = state
        with tf.variable_scope(scope or type(self).__name__):
            ref_vector = tf.concat([inputs, h_prev], -1)
            G = tf.tanh(self.fc_context
                        + tf.expand_dims(tc.layers.fully_connected(ref_vector,
                                                                   num_outputs=self._num_units,
                                                                   activation_fn=None), 1))
            logits = tc.layers.fully_connected(G, num_outputs=1, activation_fn=None)
            scores = tf.nn.softmax(logits, 1)

            attended_context = tf.reduce_sum(self.context_to_attend * scores, axis=1)
            new_inputs = tf.concat([inputs, attended_context,
                                    inputs - attended_context, inputs * attended_context],
                                   -1)
            return super(MatchLSTMAttnCell, self).__call__(new_inputs, state, scope)


class MatchLSTMLayer(object):
    """
    Implements the Match-LSTM layer, which attend to the question dynamically in a LSTM fashion.
    """
    def __init__(self, hidden_size):
        self.hidden_size = hidden_size

    def match(self, passage_encodes, question_encodes, p_length, q_length):
        """
        Match the passage_encodes with question_encodes using Match-LSTM algorithm
        """
        with tf.variable_scope('match_lstm'):
            cell_fw = MatchLSTMAttnCell(self.hidden_size, question_encodes)
            cell_bw = MatchLSTMAttnCell(self.hidden_size, question_encodes)
            outputs, state = tf.nn.bidirectional_dynamic_rnn(cell_fw, cell_bw,
                                                             inputs=passage_encodes,
                                                             sequence_length=p_length,
                                                             dtype=tf.float32,
                                                             parallel_iterations=64)
            match_outputs = tf.concat(outputs, 2)
            state_fw, state_bw = state
            c_fw, h_fw = state_fw
            c_bw, h_bw = state_bw
            match_state = tf.concat([h_fw, h_bw], 1)
        return match_outputs, match_state


class AttentionFlowMatchLayer(object):
    """
    Implements the Attention Flow layer,
    which computes Context-to-question Attention and question-to-context Attention
    """
    def __init__(self, hidden_size):
        self.hidden_size = hidden_size
        # self.W_conv1 = W_conv1
        # self.b_conv1 = b_conv1

    def match(self, passage_encodes, question_encodes, p_length, q_length,sep_q_encodes_1,sep_q_encodes_3):
        """
        Match the passage_encodes with question_encodes using Attention Flow Match algorithm
        """
        with tf.variable_scope('bidaf'):
            #基于问题的字注意力机制-1_gram
            p_mask = tf.sequence_mask(p_length,tf.shape(passage_encodes)[1],dtype=tf.floats32,name='passage_mask')
            q_mask = tf.sequence_mask(q_length,tf.shape(question_encodes)[1],dtype=tf.floats32,name='question_mask')
            q_mask_1 = tf.sequence_mask(q_length,tf.shape(sep_q_encodes_3)[1],dtype=tf.floats32,name='question_mask_1')

            sim_matrix_2 = tf.matmul(passage_encodes, question_encodes, transpose_b=True)

            context2question_attn_2 = tf.matmul(tf.nn.softmax(sim_matrix_2, -1), question_encodes)
            b_2 = tf.nn.softmax(tf.expand_dims(tf.reduce_max(sim_matrix_2, 2), 1), -1)
            question2context_attn_2 = tf.tile(tf.matmul(b_2, passage_encodes),
                                         [1, tf.shape(passage_encodes)[1], 1])

            sim_matrix_1 = tf.matmul(passage_encodes, sep_q_encodes_1, transpose_b=True)
            context2question_attn_1 = tf.matmul(tf.nn.softmax(sim_matrix_1, -1), sep_q_encodes_1)
            b_1 = tf.nn.softmax(tf.expand_dims(tf.reduce_max(sim_matrix_1, 2), 1), -1)
            question2context_attn_1 = tf.tile(tf.matmul(b_1, passage_encodes),
                                        [1, tf.shape(passage_encodes)[1], 1])

            sim_matrix_3 = tf.matmul(passage_encodes, sep_q_encodes_3, transpose_b=True)
            context2question_attn_3 = tf.matmul(tf.nn.softmax(sim_matrix_3, -1), sep_q_encodes_3)
            b_3 = tf.nn.softmax(tf.expand_dims(tf.reduce_max(sim_matrix_3, 2), 1), -1)
            question2context_attn_3 = tf.tile(tf.matmul(b_3, passage_encodes),
                                        [1, tf.shape(passage_encodes)[1], 1])

            concat_outputs = tf.concat([passage_encodes, context2question_attn_1,
                                        passage_encodes * context2question_attn_1,
                                        passage_encodes * question2context_attn_1,
                                        context2question_attn_2,
                                        passage_encodes * context2question_attn_2,
                                        passage_encodes * question2context_attn_2,
                                        context2question_attn_3,
                                        passage_encodes * context2question_attn_3,
                                        passage_encodes * question2context_attn_3,
                                        ], -1)

            # concat_outputs_extend = tf.expand_dims(concat_outputs, -1)
            # question_encodes_2 = tf.nn.relu(self.conv2d(concat_outputs_extend, self.W_conv1) + self.b_conv1)
            # question_encodes_2_poll = self.max_pool_2x1(question_encodes_2)
            # concat_outputs = tf.squeeze(question_encodes_2 , -1)




            # #基于问题的字注意力机制-2_gram
            # question_encodes_extend = tf.expand_dims(question_encodes, -1)
            # question_encodes_2 = tf.nn.relu(self.conv2d(question_encodes_extend,self.W_conv1 + self.b_conv1))
            # question_encodes_2 = tf.squeeze(question_encodes_2,-1)
            # sim_matrix_2 = tf.matmul(passage_encodes, question_encodes_2, transpose_b=True)
            #
            # context2question_attn_2 = tf.matmul(tf.nn.softmax(sim_matrix_2, -1), question_encodes_2)
            # b_2 = tf.nn.softmax(tf.expand_dims(tf.reduce_max(sim_matrix_2, 2), 1), -1)
            # question2context_attn_2 = tf.tile(tf.matmul(b_2, passage_encodes),
            #                             [1, tf.shape(passage_encodes)[1], 1])
            # concat_outputs = tf.concat([passage_encodes, context2question_attn_2,
            #                             passage_encodes * context2question_attn_2,
            #                             passage_encodes * question2context_attn_2], -1)


            # passage_context2question_attn = passage_encodes * context2question_attn
            # passage_question2context_attn = passage_encodes * question2context_attn
            # concat_tensor = tf.stack([passage_encodes, context2question_attn,passage_context2question_attn,passage_question2context_attn],-1)
            #
            # cnn_op = tf.nn.relu(self.conv2d(concat_tensor,self.W_conv1) +self.b_conv1)
            #
            # tensor_list = tf.split(cnn_op,[1,1,1,1,1,1,1,1],-1)
            #
            # for id, one_tensor in enumerate(tensor_list):
            #     one_tensor = tf.squeeze(one_tensor,-1)
            #     if id == 0:
            #         concat_outputs = one_tensor
            #     else:
            #         concat_outputs = tf.concat([concat_outputs,one_tensor],-1)




            return concat_outputs , None


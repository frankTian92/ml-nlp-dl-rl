#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__mktime__ = '2018/4/20 0020'
__author__ = 'Administrator'
__filename__ = 'test'
"""
import re


# # 获得指定元素的多有下标
# def get_all_index(x, list):
#     index_list = []
#     first = 0
#     for i in range(list.count(x)):
#         new_list = list[first:]
#         index = first + new_list.index(x)
#         index_list.append(index)
#         first = index + 1
#     return index_list
#
# #删除相同的数组
# def removeSameList(list, sub_list):
#     start_param = sub_list[0]
#     if start_param in list:
#         start_index_list = get_all_index(x=start_param, list=list)
#         del_num = 0;
#         for starts_index in start_index_list:
#             starts_index =  starts_index-del_num
#             same_num = 0
#             for id, sub_str in enumerate(sub_list):
#                 if list[starts_index + id] == sub_str:
#                     same_num += 1
#             if (same_num == len(sub_list)):
#                 for _ in range(same_num):
#                     del list[starts_index]
#                     del_num +=1
#     return list

def find_last_pos(list,last_index):
    sub_list = list[last_index:]
    for id,sub_str in enumerate(sub_list):
        if judgePunctutation(s=sub_str[-1],is_strat=False):
            return last_index+id


def judgePunctutation( s, is_strat):
    '''
    Judge whether the char is a punctuation mark.
    :param s: char
    :return: bool value
    '''
    start_regex = '[’\n 。。。!#$%&\'*+-.。/:;=\\s+？...?@^_`~+]+'
    end_regex = '[’!！.。;；...\\]】\n）)？?}>》\\s+\\"”]+'
    if is_strat:
        an = re.search(start_regex, s)
    else:
        an = re.search(end_regex, s)
    if an:
        return True
    else:
        return False

m = ["\n","那好","好的啊","我的","\n","号达 "]
index = 1
last_index = find_last_pos(list=m,last_index=index)
print(last_index)
print(m[last_index])

if judgePunctutation(m[0],True):
    best_answer = m[1:]
    print(best_answer)




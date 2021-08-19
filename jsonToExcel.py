# coding=utf-8
# !/usr/bin/env python
# coding=gbk
import sys

import pandas as pd
import json

import os.path
import re
# df = pd.read_json('1.json')

# print(df)
from pandas import DataFrame

# pathDir = os.listdir('C:/Users/liuff19/Desktop/json')  # 索引json的文件夹

'''初始化所用的参数'''
member_name = []
relation = []
leader_name = []
idcard = []
zong_num = []
leader_id = []
family_num = 0
fam = []
'''==========================================='''


# res = pd.DataFrame(columns=["宗地号"])


def info_basic_out(path):  # path 是只存放json文件的文件夹路径
    pathDir = os.listdir(path)  # 索引json的文件夹
    for s in pathDir:
        print(s)
        s = os.path.join(path, s)
        with open(s, 'r') as f:
            data = json.loads(f.read())
            df = pd.json_normalize(
                data,
                meta=['权利人姓名', '宗地号', '权利人证件编号'],
                record_path=['家庭成员'])

            # print(df)
            # print(df.iloc[:, 1].values)

            '''户内成员姓名'''
            member_name.append(list(df.iloc[:, 0].values))

            '''与户主的关系'''
            relation.append(list(df.iloc[:, 1].values))

            '''权利人姓名'''
            leader_name.append(list(df.iloc[:, 3].values))

            '''身份证号码'''
            idcard.append(list(df.iloc[:, 2].values))

            '''宗地号码'''
            zong_num.append(list(df.iloc[:, 4].values))

            '''权利人证件编号'''
            leader_id.append(list(df.iloc[:, 5].values))

            '''家庭总人数'''
            fam.append([len(df)] * len(df))




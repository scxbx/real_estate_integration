# coding=utf-8
# !/usr/bin/env python

import sys

import pandas as pd
import json

import os.path
import re
import itertools
# df = pd.read_json('1.json')

from pandas import DataFrame

# pathDir = os.listdir('C:/Users/liuff19/Desktop/json')  # 索引json的文件夹

'''初始化所用的参数'''
member_name = []
old_relation = []
relation = []
leader_name = []
leader_relation = []
# relation_error_index = 0
idcard = []
zong_num = []
leader_id = []
family_num = 0
fam = []
basic_relation_set = ["户主", "父亲", "母亲",
                      "子", "儿子", "长子", "次子",
                      "二子", "三子", "四子", "五子",
                      "女", "女儿", "长女", "次女", "二女",
                      "三女", "四女", "五女", "兄", "弟", "兄弟",
                      "哥哥", "弟弟", "姐", "妹", "姐妹", "姐姐",
                      "妹妹", "儿媳", "妻", "妻子", "弟媳", "配偶",
                      "嫂子", "孙", "孙女", "孙子", "外孙子", "外孙",
                      "外孙女", "侄子", "侄女", "外甥", "外甥女"]
'''==========================================='''


# res = pd.DataFrame(columns=["宗地号"])

def sort_file_name(a_list):
    """
    将元素为'x.json'的文数组按数字x排序

    :param a_list: 要排序的数组
    """
    def take_first(item):
        string = item.split('.')[0]
        return int(string)

    a_list.sort(key=take_first)


def info_basic_out(path):  # path 是只存放json文件的文件夹路径
    pathDir = os.listdir(path)  # 索引json的文件夹
    sort_file_name(pathDir)
    for s in pathDir:
        s = os.path.join(path, s)
        with open(s, 'r') as f:
            data = json.loads(f.read())
            print('data', data)
            df = pd.json_normalize(
                data,
                meta=['权利人姓名', '宗地号', '权利人证件编号', '权利人关系'],
                record_path=['家庭成员'])

            '''户内成员姓名'''
            member_name.append(list(df.iloc[:, 0].values))

            '''与户主的关系'''
            relation.append(list(df.iloc[:, 1].values))

            '''权利人姓名'''
            leader_name.append(list(df.iloc[:, 3].values))

            '''权利人关系'''
            leader_relation.append(list(df.iloc[:, 6].values))

            '''身份证号码'''
            idcard.append(list(df.iloc[:, 2].values))

            '''宗地号码'''
            zong_num.append(list(df.iloc[:, 4].values))

            '''权利人证件编号'''
            leader_id.append(list(df.iloc[:, 5].values))

            '''家庭总人数'''
            fam.append([len(df)] * len(df))


def obligee_is_fumu(h):  # 当权利人是户主的父亲、母亲时
    if "妻子" in h:
        h[h.index("妻子")] = "儿媳"
    if "妻" in h:
        h[h.index("妻")] = "儿媳"

    # 加入性别判断，该户主为男性则为"儿子"，女性则为女儿
    #    if "户主" in h:
    #        h[h.index("户主")] = ""

    # 加入性别判断，该配偶为男性则为"女婿"，女性则为儿媳
    #    if "配偶" in h:
    #       h[h.index("配偶")] = ""

    if "子" in h:
        h[h.index("子")] = "孙子"
    if "儿子" in h:
        h[h.index("儿子")] = "孙子"
    if "长子" in h:
        h[h.index("长子")] = "孙子"
    if "次子" in h:
        h[h.index("次子")] = "孙子"
    if "二子" in h:
        h[h.index("二子")] = "孙子"
    if "三子" in h:
        h[h.index("三子")] = "孙子"
    if "四子" in h:
        h[h.index("四子")] = "孙子"
    if "五子" in h:
        h[h.index("五子")] = "孙子"
    if "女" in h:
        h[h.index("女")] = "孙女"
    if "女二" in h:
        h[h.index("女儿")] = "孙女"
    if "长女" in h:
        h[h.index("长女")] = "孙女"
    if "次女" in h:
        h[h.index("次女")] = "孙女"
    if "二女" in h:
        h[h.index("二女")] = "孙女"
    if "三女" in h:
        h[h.index("三女")] = "孙女"
    if "四女" in h:
        h[h.index("四女")] = "孙女"
    if "五女" in h:
        h[h.index("五女")] = "孙女"


def obligee_is_qizi(h):  # 当权利人是户主的妻子时
    if "户主" in h:
        h[h.index("户主")] = "配偶"


def obligee_is_xiongdi(h):  # 当权利人是户主的兄弟时
    # 加入性别、年龄判断，该户主为男性则为"兄弟"，女性则判断年龄，大于权利人为"姐"，小于为妹
    #    if "户主" in h:
    #        h[h.index("户主")] = ""
    if "弟媳" in h:
        h[h.index("弟媳")] = "妻子"
    if "嫂子" in h:
        h[h.index("嫂子")] = "妻子"
    if "侄子" in h:
        h[h.index("侄子")] = "儿子"
    if "侄女" in h:
        h[h.index("侄女")] = "女儿"


def obligee_is_jiemei(h):  # 当权利人是户主的姐妹时
    # 加入性别、年龄判断，该户主为女性则为"姐妹"，男性则判断年龄，大于权利人为"兄"，小于为弟
    #    if "户主" in h:
    #        h[h.index("户主")] = ""
    if "外甥" in h:
        h[h.index("外甥")] = "儿子"
    if "外甥女" in h:
        h[h.index("外甥女")] = "女儿"


def obligee_is_erzi(h):  # 当权利人是户主的儿子时
    # 加入性别判断，该户主为男性则为"父亲"，女性则为母亲
    #    if "户主" in h:
    #        h[h.index("户主")] = ""
    if "妻子" in h:
        h[h.index("妻子")] = "母亲test"
    if "妻" in h:
        h[h.index("妻")] = "母亲test"
    if "父亲" in h:
        h[h.index("父亲")] = "祖父"
    if "母亲" in h:
        h[h.index("母亲")] = "祖母"
    # 加入性别判断，该配偶为男性则为"父亲"，女性则为母亲
    #    if "配偶" in h:
    #       h[h.index("配偶")] = ""
    if "子" in h:
        h[h.index("子")] = "兄弟"
    if "儿子" in h:
        h[h.index("儿子")] = "兄弟"
    if "长子" in h:
        h[h.index("长子")] = "兄弟"
    if "次子" in h:
        h[h.index("次子")] = "兄弟"
    if "二子" in h:
        h[h.index("二子")] = "兄弟"
    if "三子" in h:
        h[h.index("三子")] = "兄弟"
    if "四子" in h:
        h[h.index("四子")] = "兄弟"
    if "五子" in h:
        h[h.index("五子")] = "兄弟"
    # 加入年龄判断，小于权利人的改为"妹"，大于权利人的改为"姐"
    #    if "女" in h:
    #        h[h.index("女")] = ""
    #    if "女儿" in h:
    #        h[h.index("女儿")] = ""
    #    if "长女" in h:
    #        h[h.index("长女")] = ""
    #    if "二女" in h:
    #        h[h.index("二女")] = ""
    #    if "次女" in h:
    #        h[h.index("次女")] = ""
    #    if "三女" in h:
    #        h[h.index("三女")] = ""
    #    if "四女" in h:
    #        h[h.index("四女")] = ""
    #    if "五女" in h:
    #        h[h.index("五女")] = ""
    if "孙子" in h:
        h[h.index("孙子")] = "儿子"
    if "孙女" in h:
        h[h.index("孙女")] = "女儿"
    # 加入性别判断，该孙为男性则为儿子，女性则为女儿
    #    if "孙" in h:
    #        h[h.index("孙")] = "儿子"
    if "儿媳" in h:
        h[h.index("儿媳")] = "妻子"


def obligee_is_nver(h):  # 当权利人是户主的女儿时
    # 加入性别判断，该户主为男性则为"父亲"，女性则为母亲
    #    if "户主" in h:
    #        h[h.index("户主")] = ""
    if "妻子" in h:
        h[h.index("妻子")] = "母亲"
    if "妻" in h:
        h[h.index("妻")] = "母亲"
    if "父亲" in h:
        h[h.index("父亲")] = "祖父"
    if "母亲" in h:
        h[h.index("母亲")] = "祖母"
    # 加入性别判断，该配偶为男性则为"父亲"，女性则为母亲
    #    if "配偶" in h:
    #       h[h.index("配偶")] = ""
    if "女" in h:
        h[h.index("女")] = "姐妹"
    if "女二" in h:
        h[h.index("女儿")] = "姐妹"
    if "长女" in h:
        h[h.index("长女")] = "姐妹"
    if "次女" in h:
        h[h.index("次女")] = "姐妹"
    if "二女" in h:
        h[h.index("二女")] = "姐妹"
    if "三女" in h:
        h[h.index("三女")] = "姐妹"
    if "四女" in h:
        h[h.index("四女")] = "姐妹"
    if "五女" in h:
        h[h.index("五女")] = "姐妹"
    # 加入年龄判断，小于权利人的改为"弟"，大于权利人的改为"兄"
    #    if "子" in h:
    #        h[h.index("子")] = ""
    #    if "儿子" in h:
    #        h[h.index("儿子")] = ""
    #    if "长子" in h:
    #        h[h.index("长子")] = ""
    #    if "二子" in h:
    #        h[h.index("二子")] = ""
    #    if "次子" in h:
    #        h[h.index("次子")] = ""
    #    if "三子" in h:
    #        h[h.index("三子")] = ""
    #    if "四子" in h:
    #        h[h.index("四子")] = ""
    #    if "五子" in h:
    #        h[h.index("五子")] = ""
    if "外孙子" in h:
        h[h.index("外孙子")] = "儿子"
    if "外孙女" in h:
        h[h.index("外孙女")] = "女儿"


# 加入性别判断，该孙为男性则为儿子，女性则为女儿
#    if "外孙" in h:
#        h[h.index("外孙")] = ""


def obligee_is_sunzi(h):  # 当权利人是户主的孙子时
    # 加入性别判断，该户主为男性则为"祖父"，女性则为祖母
    #    if "户主" in h:
    #        h[h.index("户主")] = ""
    if "妻子" in h:
        h[h.index("妻子")] = "祖母"
    if "妻" in h:
        h[h.index("妻")] = "祖母"
    if "父亲" in h:
        h[h.index("父亲")] = "曾祖父"
    if "母亲" in h:
        h[h.index("母亲")] = "曾祖母"
    # 加入性别判断，该配偶为男性则为祖父，女性则为祖母
    #    if "配偶" in h:
    #       h[h.index("配偶")] = ""
    if "子" in h:
        h[h.index("子")] = "父亲"
    if "儿子" in h:
        h[h.index("儿子")] = "父亲"
    if "长子" in h:
        h[h.index("长子")] = "父亲"
    if "次子" in h:
        h[h.index("次子")] = "父亲"
    if "二子" in h:
        h[h.index("二子")] = "父亲"
    if "三子" in h:
        h[h.index("三子")] = "父亲"
    if "四子" in h:
        h[h.index("四子")] = "父亲"
    if "五子" in h:
        h[h.index("五子")] = "父亲"
    if "孙子" in h:
        h[h.index("孙子")] = "兄弟"
    # 加入年龄判断，大于权利人为姐，小于则为妹
    #    if "孙女" in h:
    #        h[h.index("孙女")] = ""
    # 加入性别、年龄判断，该孙为男性则为兄弟，女性则大于权利人为姐，小于则为妹
    #    if "孙" in h:
    #        h[h.index("孙")] = ""
    if "孙子" in h:
        h[h.index("孙子")] = "兄弟"
    if "儿媳" in h:
        h[h.index("儿媳")] = "母亲"


def relation_solu():

    relation_error_index = 0
    for hu in leader_relation:
        relation_error_index = relation_error_index + 1
        if hu[0] == "户主":  # 第一层判断：如果权利人是户主就直接跳过   ,hu[应该是权利人]
            continue
        else:
            '''下面是大批量判断部分：'''
            if hu[0] == "父亲" or hu[0] == "父":  # 0
                obligee_is_fumu(relation[relation_error_index])
            elif hu[0] == "母亲" or hu[0] == "母":
                obligee_is_fumu(relation[relation_error_index])
            elif hu[0] == "妻子" or hu[0] == "妻":
                obligee_is_qizi(relation[relation_error_index])
            elif hu[0] == "兄弟":
                obligee_is_xiongdi(relation[relation_error_index])
            elif hu[0] == "姐妹":
                obligee_is_jiemei(relation[relation_error_index])
            elif hu[0] == "儿子" or hu[0] == "长子":
                obligee_is_erzi(relation[relation_error_index])
            elif hu[0] == "女儿":
                obligee_is_nver(relation[relation_error_index])
            elif hu[0] == "孙子":
                obligee_is_sunzi(relation[relation_error_index])
            else:
                continue

    print()

def match_ref(ref_path, txt_path):
    '''将嵌套列表变成一维列表'''
    idcard_1 = list(itertools.chain.from_iterable(idcard))  # idcard_1 代表一维的列表
    leader_name_1 = list(itertools.chain.from_iterable(leader_name))
    member_name_1 = list(itertools.chain.from_iterable(member_name))
    zong_num_1 = list(itertools.chain.from_iterable(zong_num))

    msg_difference = '【家庭成员信息不一致】 1.宗地号 2.权利人 3.产改中的名字 4.识别出的名字'
    msg_lack = '【家庭成员缺漏核实】 1.宗地号 2.权利人 3.成员名字'
    msg_id_error = '家庭成员身份证核实'

    list_difference = [msg_difference]
    list_lack = [msg_lack]
    list_id_error = []


    '''对比数据部分'''
    refdata = pd.read_excel(ref_path)

    '''参考信息'''
    ref_idcard = refdata.iloc[1:, 12].values  # 参考的身份证号
    ref_allname = refdata.iloc[1:, 3].values  # 参考的姓名列表

    ref_dict = {}
    ref_dict_name_to_id = {}

    for i in range(len(ref_allname)):
        if ref_allname[i] is not None:
            ref_dict[ref_idcard[i]] = ref_allname[i].strip()
            ref_dict_name_to_id[ref_allname[i]] = ref_idcard[i]

    print('ref_dict', ref_dict)

    for i in range(len(idcard)):        # print(idcard[i])
        for j in range(len(idcard[i])):
            ref_name = ref_dict.get(idcard[i][j])
            if ref_name is not None:
                ref_name = ref_name.strip()
                if ref_name != member_name[i][j]:
                    # print("1 {} is different from {}".format(ref_name, member_name[i][j]))

                    msg = "{}\t{}\t{}\t{}".format(zong_num[i][j][-3:], leader_name[i][j], ref_name, member_name[i][j])
                    list_difference.append(msg)
                    member_name[i][j] = ref_name

    for i in range(len(member_name_1)):
        # print('ref name to id: ', ref_dict_name_to_id)
        if ref_dict_name_to_id.get(member_name_1[i]) is None:
            msg = "{}\t{}\t{}".format(zong_num_1[i][-3:], leader_name_1[i], member_name_1[i])
            print(msg)
            list_lack.append(msg)

        # else:
        #     print(member_name_1[i], 'not none')
    write_to_txt(txt_path, list_difference, list_lack)


def write_to_txt(path, list_d, list_l):
    with open(path, 'w') as f:
        for difference in list_d:
            f.write(difference + '\n')

        for lack in list_l:
            f.write(lack + '\n')


if __name__ == '__main__':
    print('Hello world!')
    info_basic_out(r'C:\Users\sc\Documents\飞行者科技\房地一体\各种测试\关系')
    print("relation1", relation)
    relation_solu()
    print("relation2", relation)
    match_ref(r'refsrc.xlsx')



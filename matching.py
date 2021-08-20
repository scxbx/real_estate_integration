from pandas import DataFrame

from jsonToExcel import info_basic_out
from jsonToExcel import member_name
from jsonToExcel import idcard
from jsonToExcel import zong_num
from jsonToExcel import relation
import pandas as pd
from jsonToExcel import leader_name
import itertools

'''记录错误信息的列表'''
list_for_errorID = []
list_for_errorname = []

list_difference = []
list_lack = []
list_id_error = []

msg_difference = '家庭成员信息不一致'
msg_lack = '家庭成员缺漏核实'
msg_id_error = '家庭成员身份证核实'

'''对身份证号匹配的处理'''


def idnum_solution():
    for soluid in idcard_1:
        if soluid in ref_idcard:
            list_for_errorID.append(1)
        else:
            list_for_errorID.append(0)

    errorID_index_out = [i for i, x in enumerate(list_for_errorID) if x == 0]  # 错误身份证号对应的索引
    errorID_leader_name = []  # 错误身份证号对应的权利人姓名
    errorID_zong_num = []
    for i in errorID_index_out:
        errorID_leader_name.append(leader_name_1[i])
        errorID_zong_num.append(zong_num_1[i][-5:])

    error_id_toexcel = {
        "错误的身份证号位置": errorID_index_out,
        "错误身份证号对应的权利人姓名": errorID_leader_name,
        "宗地号后5位": errorID_zong_num
    }

    DataFrame(error_id_toexcel).to_excel('error_身份证号.xlsx')
    '''========================================================'''


'''对姓名匹配的处理'''


def eachname_solution():
    for soluname in member_name_1:
        if soluname in ref_allname:
            list_for_errorname.append(1)
        else:
            list_for_errorname.append(0)

    errorName_index_out = [i for i, x in enumerate(list_for_errorname) if x == 0]
    errorName_leader_name = []
    errorName_zong_num = []
    for i in errorName_index_out:
        errorName_leader_name.append(leader_name_1[i])
        errorName_zong_num.append(zong_num_1[i][-5:])

    error_Name_toexcel = {
        "错误的姓名位置": errorName_index_out,
        "错误的姓名对应的权利人": errorName_leader_name,
        "宗地号后5位": errorName_zong_num
    }
    DataFrame(error_Name_toexcel).to_excel('error_全部姓名.xlsx')


'''================================'''

'''对家庭关系的处理'''


if __name__ == '__main__':
    info_basic_out(r'C:\Users\sc\PycharmProjects\real_estate_integration\json\2021-08-19 14-16-59')

    '''将嵌套列表变成一维列表'''
    idcard_1 = list(itertools.chain.from_iterable(idcard))  # idcard_1 代表一维的列表
    leader_name_1 = list(itertools.chain.from_iterable(leader_name))
    member_name_1 = list(itertools.chain.from_iterable(member_name))
    zong_num_1 = list(itertools.chain.from_iterable(zong_num))


    '''对比数据部分'''
    refdata = pd.read_excel('refsrc.xlsx')

    '''参考信息'''
    ref_idcard = refdata.iloc[1:, 12].values  # 参考的身份证号
    ref_allname = refdata.iloc[1:, 3].values  # 参考的姓名列表

    ref_dict = {}

    for i in range(len(ref_allname)):
        if ref_allname[i] is not None:
            ref_dict[ref_idcard[i]] = ref_allname[i]

    print('ref_dict', ref_dict)
    '''=========================================='''

    # for i in range(len(idcard_1)):
    #     ref_name = ref_dict.get(idcard_1[i])
    #     if ref_name is not None:
    #         ref_name = ref_name.strip()
    #         if ref_name != member_name_1[i]:
    #             # print("{} is different from {}".format(ref_name, member_name_1[i]))
    #             # ①若存在不一致的情况以
    #             # 【宗地号】最后三位+【权利人姓名】:【家庭成员1】+【家庭成员1关系】+【家庭成员1身份证号】、
    #             # 【家庭成员2】+【家庭成员2关系】+【家庭成员2身份证号】、...
    #             member_name_1[i] = ref_name
    #             msg = "{} {} 产改：{} 识别：{}".format(zong_num_1[i][-3:], leader_name_1[i], ref_name, member_name_1[i])
    #             list_difference.append(msg)

    for i in range(len(idcard)):
        # print(idcard[i])
        for j in range(len(idcard[i])):
            ref_name = ref_dict.get(idcard[i][j])
            if ref_name is not None:
                ref_name = ref_name.strip()
                if ref_name != member_name[i][j]:
                    print("1 {} is different from {}".format(ref_name, member_name[i][j]))
                    member_name[i][j] = ref_name

    idnum_solution()
    eachname_solution()


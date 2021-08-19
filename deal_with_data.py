# coding=utf-8

# coding=gbk
import os

import pandas as pd

import check_id
import json
import openpyxl
import jsonToExcel
import tkinter as tk

# df = pd.read_json('1.json')

# print(df)
from pandas import DataFrame

import ocr_id
from parcel_property_sheet import get_max_row

msg_error = []


def write_into_excel(in_path, out_path):
    wb = openpyxl.load_workbook(in_path, data_only=True)
    ws = wb['Sheet1']

    row = 3
    for i in range(len(jsonToExcel.member_name)):
        members_num = len(jsonToExcel.member_name[i])
        for j in range(members_num):
            def fill_and_merge(my_col, my_list):
                if j == 0:
                    # print('row', row)
                    ws.cell(row, my_col).value = my_list[i][j]
                    # print('row2', row)
                    ws.merge_cells(start_row=row, start_column=my_col, end_row=row + members_num - 1, end_column=my_col)

            id_number = jsonToExcel.idcard[i][j]
            check_id.check_id(id_number, row)

            # 宗地号 A 1
            fill_and_merge(1, jsonToExcel.zong_num)

            # 户主 B2
            fill_and_merge(2, jsonToExcel.leader_name)
            # 家庭总人数 C3
            fill_and_merge(3, jsonToExcel.fam)
            # 户内成员姓名    D4
            ws.cell(row, 4).value = jsonToExcel.member_name[i][j]
            # 与户主关系     E5
            ws.cell(row, 5).value = jsonToExcel.relation[i][j]
            # 性别    H 8
            ws.cell(row, 8).value = get_gender_from_id(id_number, row)
            # 出生日期  J 10
            ws.cell(row, 10).value = get_birthday_from_id(id_number)
            # 身份证号  M 13
            ws.cell(row, 13).value = id_number
            # 年龄    N 14
            ws.cell(row, 14).value = get_age_from_id(id_number)
            # 备注    R

            row += 1

    wb.save(out_path)
    wb.close()

    clear_data()
    print('写入{}完成'.format(out_path))


def clear_data():
    jsonToExcel.member_name = []
    jsonToExcel.relation = []
    jsonToExcel.leader_name = []
    jsonToExcel.idcard = []
    jsonToExcel.zong_num = []
    jsonToExcel.leader_id = []
    jsonToExcel.family_num = 0
    jsonToExcel.fam = []


def get_age_from_id(id_number):
    if id_number is None:
        return ''
    if len(id_number) != 18:
        return ''

    year = id_number[6:10]
    if year.isdigit():
        year = int(year)
        age = 2021 - year
        return age
    else:
        return ''


def get_birthday_from_id(id_number):
    if id_number is None:
        return ''
    if len(id_number) != 18:
        return ''
    year = id_number[6:10]
    month = id_number[10:12]
    day = id_number[12:14]
    return '{}年{}月{}日'.format(year, month, day)


def get_gender_from_id(id_number, row):
    if id_number is None:
        return ''
    if len(id_number) != 18:
        return ''
    gender_num = id_number[-2]
    if gender_num.isdigit():
        gender_num = int(gender_num)
        if gender_num % 2 == 1:
            return '男'
        else:
            return '女'
    else:
        msg_error.append('第{}行身份证倒数第二位不为数字，无法识别男女'.format(row))
        return ''


def read_jsons_to_list(path):
    files = os.listdir()
    my_list = []
    for file in files:
        if '.json' in file:
            full_path = os.path.join(path, file)
            with open(full_path, 'r') as f:
                temp = json.loads(f.read())
                my_list.append(temp)
                # print(temp)

    return my_list


def write_error_msg(alist, apath):
    with open(apath, 'w+') as f:
        for i in alist:
            f.write(i + '\n')


class App(tk.Tk):
    """
        使用tk的简单gui。用于：
        1. 通过ocr获取由每个家庭的字典组成的数组，并保存过程中的json文件
        2. 通过保存的json文件，直接生成由每个家庭的字典组成的数组
        3. 通过上述数组，生成挂接表
    """

    list_families = []
    sample_path = ''
    out_path = ''
    json_dir = ''

    def __init__(self, sample_path, out_path):
        super().__init__()
        self.sample_path = sample_path
        self.out_path = out_path

        def ocr_to_list():
            self.list_families = ocr_id.get_family(True)
            self.json_dir = self.list_families[1]

        def json_to_list():
            self.list_families = ocr_id.get_family(False)
            self.json_dir = self.list_families[1]

        def list_to_excel():
            print(self.json_dir)
            my_json_path = r'C:\Users\sc\PycharmProjects\real_estate_integration\2021-08-19 09-31-12'
            my_json_path = self.json_dir
            print(my_json_path)
            jsonToExcel.info_basic_out(my_json_path)
            path_time = os.path.join('结果', my_json_path)
            if not os.path.exists(path_time):
                os.makedirs(path_time)
            write_into_excel(self.sample_path, os.path.join(path_time, '挂接表.xlsx'))
            check_id.write_id_error_file(os.path.join(path_time, '身份证检查结果.txt'))

        # def json_on_text():
        #     for family in self.list_families:
        #         text1.insert('end', family)

        tk.Button(self, text="OCR识别", command=ocr_to_list).pack()
        tk.Button(self, text="本地数据", command=json_to_list).pack()
        tk.Button(self, text="写入excel", command=list_to_excel).pack()
        # text1 = tk.Text(self, width=65, height=30)
        #
        # scroll = tk.Scrollbar()
        # # 将滚动条填充
        # scroll.pack(side=tk.RIGHT, fill=tk.Y)  # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
        #
        # # 将滚动条与文本框关联
        # scroll.config(command=text1.yview)  # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
        # text1.config(yscrollcommand=scroll.set)  # 将滚动条关联到文本框
        #
        # text1.pack()


if __name__ == '__main__':
    # a_dict = get_col_data()

    # list_m = read_jsons_to_list(r'C:\Users\sc\PycharmProjects\real_estate_integration')
    # print(list_m)
    # path = r'C:\Users\sc\PycharmProjects\real_estate_integration\json'
    # jsonToExcel.info_basic_out(path)
    # print(jsonToExcel.idcard)
    #
    # write_into_excel(r'C:\Users\sc\Documents\飞行者科技\房地一体\sample.xlsx',
    #                  r'C:\Users\sc\Documents\飞行者科技\房地一体\挂接表out.xlsx')

    in_path = r'默认表格\挂接表模板.xlsx'
    out_path = r'结果\挂接表'
    app = App(in_path, out_path)
    app.mainloop()

    # path = r'C:\Users\sc\PycharmProjects\real_estate_integration\2021-08-18 17-52-08'
    # jsonToExcel.info_basic_out(path)
    # write_into_excel(in_path, out_path)

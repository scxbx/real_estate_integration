#!/usr/bin/python
from datetime import datetime
from datetime import timedelta

import json
import os
import re

# line = "Cats are smarter than dogs"
# matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)
# if matchObj:
#     print("matchObj.group() : ", matchObj.group())
#     print("matchObj.group(1) : ", matchObj.group(1))
#     print("matchObj.group(2) : ", matchObj.group(2))
# else:
#     print("No match!!")


import deal_with_data
import jsonToExcel
import ocr_id
import parcel_property_sheet
import tkinter.filedialog


def sum_dict(a, b):
    temp = dict()
    # dict_keys类似set； | 并集
    for key in a.keys() | b.keys():
        temp[key] = sum([d.get(key, 0) for d in (a, b)])
    return temp


if __name__ == '__main__':
    # import datetime
    #
    # currentDT = datetime.datetime.now()
    #
    # print(currentDT.strftime("%Y-%m-%d %H:%M:%S"))
    # print(currentDT.strftime("%Y/%m/%d"))
    # print(currentDT.strftime("%H:%M:%S"))
    # print(currentDT.strftime("%I:%M:%S %p"))
    # print(currentDT.strftime("%a, %b %d, %Y"))
    # string = currentDT.strftime("%Y-%m-%d %H-%M-%S")
    #
    # if not os.path.exists(string):
    #     os.mkdir(string)
    # with open(os.path.join(string, '1'), 'w+') as f:
    #
    #     f.write('hello' + '\n')

    # print('hello')
    # path = r'E:/照片核对/礼亭4/02电子档案\110000001001JC00001郭团结\2-1户口本.jpg'
    # l1 = os.path.split(path)
    # print(l1)
    # l2 = os.path.split(l1[0])
    # print(l2[1][14:] + ' ' + l1[1])
    #
    # code_and_name = os.path.split(os.path.split(path)[0])[1][14:] + os.path.split(path)[1]
    # print(code_and_name)

    # my_dict = {('子', '妻'): '母亲'}
    #
    # print(my_dict.get(('子', '妻')))
    #
    # print(json.dumps(my_dict))

    # path = r'ddadf\daa\333/挂接表.xlsx'
    #
    # new = os.path.splitext(path)[0] + 'new.xlsx'
    # print(new)
    #
    # tkinter.filedialog.askdirectory()

    with open(r'默认表格\config.txt', encoding='utf-8') as f:
        content = json.loads(f.read())

    print(content.get('调查员'))
    print(content.get('测量人'))
    print(type(content))


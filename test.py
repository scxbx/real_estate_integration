#!/usr/bin/python
import datetime
import os
import re
from tkinter import filedialog

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

    print('hello')
    path = filedialog.askdirectory()
    pl = os.listdir(path)
    print('old', pl)
    jsonToExcel.sort_file_name(pl)
    print('new', pl)

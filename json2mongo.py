import os

import json
from pymongo import MongoClient

import jsonToExcel
from deal_with_data import write_into_excel


def import_json(col, folder, village_group_name):
    # Loading or Opening the json file
    data_list = []
    files = os.listdir(folder)
    for file in files:
        if not os.path.isdir(file):
            with open(os.path.join(folder, file)) as f:
                file_data = json.load(f)
                file_data['村小组'] = village_group_name
                data_list.append(file_data)

    # Inserting the loaded data in the Collection
    # if JSON contains data more than one entry
    # insert_many is used else insert_one is used
    if isinstance(data_list, list):
        col.insert_many(data_list)
    else:
        col.insert_one(data_list)


def db2excel(col, village_group):
    for data in col.find({"村小组": village_group}).sort("宗地号"):
        # print(data)
        # print(type(data))
        jsonToExcel.info_basic_out_db(data)

    write_into_excel(r'默认表格\挂接表模板.xlsx', r'结果\挂接表.xlsx')


if __name__ == '__main__':
    # Making Connection
    myclient = MongoClient("mongodb://localhost:27017/")

    # database
    db = myclient["GFG"]

    # Created or Switched to collection
    # names: GeeksForGeeks
    mycol = db["data"]
    # name = '沟上村'
    # import_json(r'C:\Users\sc\PycharmProjects\real_estate_integration\json\沟上村', name)
    # for item in mycol.find({"权利人关系": None}):
    #     print(item)

    db2excel(mycol, "沟上村")

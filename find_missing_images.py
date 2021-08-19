import json
import os
import re
import tkinter.filedialog

import ocr_id


def get_family_files(family_path):
    identification_1 = 0
    household_2 = 0
    house_4 = 0
    other_7 = 0
    for root, dirs, files in os.walk(family_path):
        for file in files:
            if file.endswith(".jpg"):
                # print(file)
                type_num = check_image_type(file)
                if type_num == '1':
                    identification_1 += 1
                elif type_num == '2':
                    household_2 += 1
                elif type_num == '4':
                    house_4 += 1
                elif type_num == '7':
                    other_7 += 1
                else:
                    print("照片名称第一个数字不为1、2、4、7中任何一个！")

    my_list = [os.path.basename(family_path)[16:], identification_1, household_2, house_4, other_7]
    print(my_list)
    return my_list


def get_all_files(all_path):
    old_list = []
    ocr_no_id = []
    dif_id = []
    wrong_files = []
    miss1 = []
    miss2 = []
    miss4 = []
    miss4_w = []
    miss12 = []
    miss24_w = []
    miss14 = []
    miss14_w = []
    miss24 = []
    miss124 = []
    miss124_w = []

    msg_ocr_no_id = '文字识别身份证失败'
    msg_wrong_file = '错误文件'
    msg124 = '缺少身份证、户口本、房屋照片'
    msg124_w = '缺少身份证、户口本，房屋照片数量不正确'
    msg12 = '缺少身份证、户口本'
    msg24 = '缺少户口本、房屋照片'
    msg14 = '缺少身份证、房屋照片'
    msg24_w = '缺少户口本，房屋照片数量不正确'
    msg14_w = '缺少身份证，房屋照片数量不正确'
    msg1 = '缺少身份证'
    msg2 = '缺少户口本'
    msg4 = '缺少房屋照片'
    msg4_w = '房屋照片数量不正确'
    msg_dif_id = '权利人姓名错误'
    new_file_name = "照片检查结果.txt"

    if os.path.exists(new_file_name):
        f = open(new_file_name, 'w')
    else:
        f = open(new_file_name, "x")
    for cur_file in os.listdir(all_path):
        full_path = os.path.join(all_path, cur_file)
        if os.path.isdir(full_path):
            print("full_path: ", full_path)
            old_list = get_family_files(full_path)
            new_list = [str(i) for i in old_list]
            f.write("\n")
            f.write(' '.join(new_list))

            name = old_list[0]
            if '_bak' in name:
                wrong_files.append(name)
            elif old_list[1] == 0 and old_list[2] == 0 and old_list[3] == 0:
                miss124.append(name)
            elif old_list[1] == 0 and old_list[2] == 0 and old_list[3] < 4:
                miss124_w.append(name)
            elif old_list[1] == 0 and old_list[2] == 0:
                miss12.append(name)
            elif old_list[1] == 0 and old_list[3] == 0:
                miss14.append(name)
            elif old_list[1] == 0 and old_list[3] < 4:
                miss14_w.append(name)
            elif old_list[2] == 0 and old_list[3] == 0:
                miss24.append(name)
            elif old_list[2] == 0 and old_list[3] < 4:
                miss24_w.append(name)
            else:
                if old_list[1] == 0:
                    miss1.append(name)
                if old_list[2] == 0:
                    miss2.append(name)
                if old_list[3] == 0:
                    miss4.append(name)
                elif old_list[3] < 4:
                    miss4_w.append(name)

            if old_list[1] != 0:
                f_filename = os.path.join(full_path, "1-1身份证明.jpg")
                print('f_filename', f_filename)
                # resp_json = ocr_id.get_householder_name(f_filename)
                resp_json = ocr_id.get_dict_from_json_file(f_filename)
                print('resp_json', resp_json)
                # if resp_json is not None and resp_json["words_result"] is not None and resp_json["words_result"]["姓名"] is not None:
                #     name_from_ocr = resp_json.get()
                if resp_json is not None:
                    print('resp_json is not None')
                    print('json', resp_json.get('words_result'))
                    if resp_json.get('words_result') is not None:
                        print('resp_json.get("words_result") is not None')
                        print('words_results', resp_json.get('words_result'))
                        if resp_json.get('words_result').get('姓名') is not None:
                            print('resp_json.get("words_result").get("姓名") is not None')
                            print('name', resp_json.get('words_result').get('姓名'))
                            if resp_json.get('words_result').get('姓名').get('words') is not None:
                                name_from_ocr = resp_json.get('words_result').get('姓名').get('words')
                                print('name_from_ocr', name_from_ocr)
                                print('old_list[0][3:]', old_list[0][3:])
                                if name_from_ocr != old_list[0][3:]:
                                    print("户主姓名和身份证不同！")
                                    dif_id.append(old_list[0])
                                if resp_json.get('words_result').get('公民身份号码').get('words') is not None:
                                    if resp_json.get('words_result').get('公民身份号码').get('words') == '':
                                        ocr_no_id.append(old_list[0])
                            else:
                                print('resp_json.get("words_result").get("姓名").get("words") is None')
                                ocr_no_id.append(old_list[0])
                        else:
                            print('resp_json.get("words_result").get("姓名") is None')
                            ocr_no_id.append(old_list[0])
                    else:
                        print('resp_json.get("words_result") is None')
                        ocr_no_id.append(old_list[0])
                else:
                    print('resp_json is None')
                    ocr_no_id.append(old_list[0])

    f.close()
    print("miss124", miss124)
    print("miss124_w", miss124_w)
    print("miss12", miss12)
    print("miss14", miss14)
    print("miss14_w", miss14_w)
    print("miss24", miss24)
    print("miss24_w", miss24_w)
    print("miss1", miss1)
    print("miss2", miss2)
    print("miss4", miss4)
    print("miss4_w", miss4_w)

    exam_images_file_name = "输出到照片资料检查.txt"
    if os.path.exists(exam_images_file_name):
        f_exam = open(exam_images_file_name, 'w')
    else:
        f_exam = open(exam_images_file_name, "x")

    write_list(f_exam, ocr_no_id, msg_ocr_no_id)
    write_list(f_exam, dif_id, msg_dif_id)
    write_list(f_exam, wrong_files, msg_wrong_file)
    write_list(f_exam, miss124, msg124)
    write_list(f_exam, miss124_w, msg124_w)
    write_list(f_exam, miss12, msg12)
    write_list(f_exam, miss14, msg14)
    write_list(f_exam, miss14_w, msg14_w)
    write_list(f_exam, miss24, msg24)
    write_list(f_exam, miss24_w, msg24_w)
    write_list(f_exam, miss1, msg1)
    write_list(f_exam, miss2, msg2)
    write_list(f_exam, miss4, msg4)
    write_list(f_exam, miss4_w, msg4_w)

    f_exam.close()


def check_image_type(image_name):
    return re.match('(.*)-(.*).jpg', image_name).group(1)


def write_list(my_file, my_list, my_str):
    if len(my_list) != 0:
        my_file.write('【' + my_str + '】\n')
        my_file.write(' '.join(my_list) + '\n\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # path = r"C:\Users\sc\Documents\飞行者科技\房地一体\测试数据\46坡田仔\02电子档案"
    # # get_family_files(path)
    # get_all_files(path)
    my_dir = tkinter.filedialog.askdirectory()
    print(my_dir)
    get_all_files(my_dir)

    # some JSON:
    # resp_json = ocr_id.get_householder_name("text.jpg")

    # parse x:
    # js = json.loads(json.dumps(eval(x)))

    # the result is a Python dictionary:
    # name_from_ocr = resp_json["words_result"]["姓名"]['words']
